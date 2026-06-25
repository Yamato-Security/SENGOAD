#!/usr/bin/env python3
"""
Offline preflight checks for the lab configs.

Validates that a lab (or a reskin of one) is internally consistent *before* you
spend time standing up VMs. It catches the failure modes a rename/reskin tends
to introduce:

  - a user / group / host reference that no longer resolves (orphaned by a rename)
  - data/inventory `domain_name=` not matching the lab folder name
    (ansible reads `ad/{{domain_name}}/data/`, so they MUST match)
  - the inventory [domain] host list not matching the config host keys
  - malformed JSON in a config.json, or malformed YAML in a playbook/role
  - a lab with no providers (the tool can't load it)

It does NOT deploy anything and needs no hypervisor/cloud. Only the Python
standard library is required; PyYAML is used for the YAML checks if available.

Usage:
    python3 scripts/preflight.py            # check every lab + extension
    python3 scripts/preflight.py SENGOAD    # check one lab (by folder name)

Exit code is non-zero if any check fails (suitable for CI).
"""
import json, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Well-known principals that always resolve (not defined in config.json).
BUILTINS = {x.lower() for x in [
    "Administrator", "Administrators", "Domain Admins", "Domain Users",
    "Domain Computers", "Domain Controllers", "Enterprise Admins", "Schema Admins",
    "Protected Users", "Guests", "Remote Desktop Users", "Users", "Account Operators",
    "Server Operators", "Backup Operators", "Print Operators", "IIS_IUSRS",
    "Cert Publishers", "Group Policy Creator Owners", "Read-only Domain Controllers",
    "Cryptographic Operators", "Distributed COM Users", "Performance Monitor Users",
    "Event Log Readers", "DnsAdmins", "Authenticated Users", "Everyone", "SYSTEM",
    "ANONYMOUS LOGON", "Key Admins", "Enterprise Key Admins",
    "Cloneable Domain Controllers", "LinuxAdmins", "LinuxUsers",
]}

GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
def ok(m):   print(f"  [{GREEN} OK {RESET}] {m}")
def fail(m): print(f"  [{RED}FAIL{RESET}] {m}")
def warn(m): print(f"  [{YELLOW}WARN{RESET}] {m}")

PROBLEMS = 0
def problem(m):
    global PROBLEMS
    PROBLEMS += 1
    fail(m)

# ---------------------------------------------------------------- helpers
def load_json(path):
    """Parse config.json; tolerate (but warn about) a trailing comma."""
    raw = open(path, encoding="utf-8").read()
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        fixed = re.sub(r",(\s*[}\]])", r"\1", raw)
        try:
            data = json.loads(fixed)
            return data, "trailing comma (technically invalid JSON)"
        except json.JSONDecodeError as e:
            return None, f"invalid JSON: {e}"

def container(data):
    return data.get("lab") or data.get("lab_extension") or {}

def basename(p):           # strip DOMAIN\ or domain.local\ prefix
    return p.split("\\")[-1].strip()

def is_special(p):         # computer$, a DN, or an NT AUTHORITY principal
    return p.split("\\")[-1].endswith("$") \
        or any(t in p for t in ("DC=", "CN=", "OU=")) \
        or p.upper().startswith("NT AUTHORITY")

def collect_defs(lab):
    users, groups, ous, domains = set(), set(), set(), set(lab.get("domains", {}))
    for dd in lab.get("domains", {}).values():
        users |= {u.lower() for u in dd.get("users", {})}
        for scope in ("universal", "global", "domainlocal"):
            groups |= {g.lower() for g in dd.get("groups", {}).get(scope, {})}
        ous |= {o.lower() for o in dd.get("organisation_units", {})}
    return users, groups, ous, domains

def collect_refs(lab):
    refs = []
    for hk, h in lab.get("hosts", {}).items():
        for g, members in (h.get("local_groups") or {}).items():
            for m in members:
                refs.append((f"host {hk} local_group '{g}'", m))
        m = h.get("mssql")
        if m:
            for s in m.get("sysadmins", []):
                refs.append((f"host {hk} mssql sysadmin", s))
            for k in (m.get("executeaslogin") or {}):
                refs.append((f"host {hk} mssql exec-login", k))
            for v in (m.get("executeasuser") or {}).values():
                refs.append((f"host {hk} mssql exec-user", v.get("user", "")))
            for ls in (m.get("linked_servers") or {}).values():
                for um in ls.get("users_mapping", []):
                    refs.append((f"host {hk} linked-server", um.get("local_login", "")))
    for dn, dd in lab.get("domains", {}).items():
        for scope in ("universal", "global", "domainlocal"):
            for gname, g in (dd.get("groups", {}).get(scope, {}) or {}).items():
                if g.get("managed_by"):
                    refs.append((f"{dn} group '{gname}' managed_by", g["managed_by"]))
                for mem in g.get("members", []):
                    refs.append((f"{dn} group '{gname}' member", mem))
        for gname, mems in (dd.get("multi_domain_groups_member") or {}).items():
            for mem in mems:
                refs.append((f"{dn} multidomain '{gname}'", mem))
        for r in (dd.get("laps_readers") or []):
            refs.append((f"{dn} laps_reader", r))
        for aname, a in (dd.get("acls") or {}).items():
            refs.append((f"{dn} acl '{aname}' .for", a.get("for", "")))
            refs.append((f"{dn} acl '{aname}' .to", a.get("to", "")))
        for uname, u in (dd.get("users", {}) or {}).items():
            for grp in u.get("groups", []):
                refs.append((f"{dn} user '{uname}' group", grp))
    return refs

# ---------------------------------------------------------------- checks
def discover_labs():
    labs = []
    for d in sorted(glob.glob(os.path.join(ROOT, "ad", "*"))):
        name = os.path.basename(d)
        if name == "TEMPLATE":
            continue
        if os.path.isfile(os.path.join(d, "data", "config.json")):
            labs.append(name)
    return labs

def global_principals(labs):
    """Union of all labs' users+groups, used to resolve extension overlay refs."""
    users, groups = set(), set()
    for lab in labs:
        data, _ = load_json(os.path.join(ROOT, "ad", lab, "data", "config.json"))
        if data:
            u, g, _, _ = collect_defs(container(data))
            users |= u
            groups |= g
    return users, groups

def check_config(path, extra_known=frozenset(), strict_topology=True):
    data, note = load_json(path)
    rel = os.path.relpath(path, ROOT)
    if data is None:
        problem(f"{rel}: {note}")
        return
    if note:
        warn(f"{rel}: {note}")
    lab = container(data)
    users, groups, ous, domains = collect_defs(lab)
    known = users | groups | ous | BUILTINS | {p.lower() for p in extra_known}
    bad = []
    for where, principal in collect_refs(lab):
        if not principal or is_special(principal):
            continue
        if basename(principal).lower() not in known:
            bad.append((where, principal))
    if strict_topology:
        for hk, h in lab.get("hosts", {}).items():
            if h.get("domain") and domains and h["domain"] not in domains:
                bad.append((f"host {hk}", f"domain '{h['domain']}' not defined in this lab"))
        for dn, dd in lab.get("domains", {}).items():
            if dd.get("dc") and dd["dc"] not in lab.get("hosts", {}):
                bad.append((f"domain {dn}", f"dc '{dd['dc']}' is not a defined host"))
    if bad:
        problem(f"{rel}: {len(bad)} unresolved reference(s)")
        for where, p in bad[:25]:
            print(f"          - {where}: '{p}'")
    else:
        ok(rel)

def check_domain_name(lab):
    inv = os.path.join(ROOT, "ad", lab, "data", "inventory")
    if not os.path.isfile(inv):
        warn(f"{lab}: no data/inventory")
        return
    m = re.search(r"^\s*domain_name\s*=\s*(\S+)", open(inv).read(), re.M)
    if not m:
        warn(f"{lab}: data/inventory has no domain_name=")
        return
    if m.group(1) == lab:
        ok(f"{lab}: domain_name == folder name ('{lab}')")
    else:
        problem(f"{lab}: domain_name='{m.group(1)}' != folder '{lab}' "
                f"(ansible resolves ad/{m.group(1)}/data/ -> would fail)")

def check_inventory_hosts(lab):
    inv = os.path.join(ROOT, "ad", lab, "data", "inventory")
    cfg = os.path.join(ROOT, "ad", lab, "data", "config.json")
    if not (os.path.isfile(inv) and os.path.isfile(cfg)):
        return
    # union hosts across every group except [*:vars] (linux hosts live in
    # [linux_domain], not [domain], so a single-section check is too strict)
    inv_hosts, section = set(), None
    for line in open(inv, encoding="utf-8"):
        s = line.strip()
        if not s or s[0] in ";#":
            continue
        head = re.match(r"\[([^\]]+)\]", s)
        if head:
            section = head.group(1)
            continue
        if section and not section.endswith(":vars") and "=" not in s:
            inv_hosts.add(s.split()[0])
    data, _ = load_json(cfg)
    cfg_hosts = set(container(data).get("hosts", {})) if data else set()
    missing, extra = cfg_hosts - inv_hosts, inv_hosts - cfg_hosts
    if not missing and not extra:
        ok(f"{lab}: inventory hosts == config hosts ({sorted(cfg_hosts)})")
        return
    if missing:  # a config host with nowhere to deploy -> real problem
        problem(f"{lab}: config hosts missing from inventory: {sorted(missing)}")
    if extra:    # usually extension hosts (elk, ws01, ...) pre-listed for add-ons
        warn(f"{lab}: inventory lists host(s) not in base config "
             f"(usually extension hosts): {sorted(extra)}")

def check_providers(lab):
    pdir = os.path.join(ROOT, "ad", lab, "providers")
    provs = [os.path.basename(p) for p in glob.glob(os.path.join(pdir, "*")) if os.path.isdir(p)]
    if provs:
        ok(f"{lab}: providers = {sorted(provs)}")
    else:
        problem(f"{lab}: no providers/ — the tool cannot load this lab")

def check_yaml():
    try:
        import yaml
    except ImportError:
        warn("PyYAML not installed — skipping YAML validation "
             "(run inside the venv to enable)")
        return
    files = glob.glob(os.path.join(ROOT, "ansible", "**", "*.yml"), recursive=True)
    files += glob.glob(os.path.join(ROOT, "ad", "*", "providers", "ludus", "config.yml"))
    files += glob.glob(os.path.join(ROOT, "extensions", "*", "providers", "ludus", "config.yml"))
    files += [os.path.join(ROOT, "playbooks.yml")]
    bad = 0
    for f in files:
        if not os.path.isfile(f):
            continue
        try:
            list(yaml.safe_load_all(open(f, encoding="utf-8")))
        except Exception as e:
            problem(f"{os.path.relpath(f, ROOT)}: invalid YAML: {e}")
            bad += 1
    if not bad:
        ok(f"{len(files)} YAML files parse cleanly")

# ---------------------------------------------------------------- main
def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    labs = discover_labs()
    if only:
        if only not in labs:
            print(f"unknown lab '{only}'. available: {labs}")
            return 2
        labs = [only]
    print(f"Preflight on {ROOT}")
    print(f"Labs: {labs}\n")

    print("== config referential integrity (labs) ==")
    for lab in labs:
        check_config(os.path.join(ROOT, "ad", lab, "data", "config.json"))

    if not only:
        print("\n== config referential integrity (extensions, resolved against all labs) ==")
        gusers, ggroups = global_principals(labs)
        for cfg in sorted(glob.glob(os.path.join(ROOT, "extensions", "*", "data", "config.json"))):
            check_config(cfg, extra_known=gusers | ggroups, strict_topology=False)

    print("\n== domain_name == folder name ==")
    for lab in labs:
        check_domain_name(lab)

    print("\n== inventory hosts == config hosts ==")
    for lab in labs:
        check_inventory_hosts(lab)

    print("\n== each lab has providers ==")
    for lab in labs:
        check_providers(lab)

    print("\n== YAML validity ==")
    check_yaml()

    print()
    if PROBLEMS:
        print(f"{RED}PREFLIGHT FAILED: {PROBLEMS} problem(s).{RESET}")
        return 1
    print(f"{GREEN}PREFLIGHT PASSED.{RESET} "
          f"(static checks only — a live VM deploy still needs your hypervisor/cloud)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
