import os
import re
from jinja2 import Environment, FileSystemLoader

version_match=re.compile("^v[0-9]+.[0-9]+.[0-9]+$")

PLUGINS = {
    'netbox_bgp': {
        'url': 'https://github.com/netbox-community/netbox-bgp',
        'dir': 'netbox-bgp',
        'pip': 'netbox-bgp'
    },
    'netbox_acls': {
        'url': 'https://github.com/netbox-community/netbox-acls',
        'dir': 'netbox-acls',
        'pip': 'netbox-acls'
    },
    'netbox_topology_views': {
        'url': 'https://github.com/netbox-community/netbox-topology-views',
        'dir': 'netbox-topology-views',
        'pip': 'netbox-topology-views'
    },
    'netbox_inventory': {
        'url': 'https://github.com/ArnesSI/netbox-inventory',
        'dir': 'netbox-inventory',
        'pip': 'netbox-inventory'
    },
    'netbox_floorplan': {
        'url': 'https://github.com/netbox-community/netbox-floorplan-plugin',
        'dir': 'netbox-floorplan-plugin',
        'pip': 'netbox-floorplan-plugin'
    },
    'netbox_dns': {
        'url': 'https://github.com/peteeckel/netbox-plugin-dns',
        'dir': 'netbox-plugin-dns',
        'pip': 'netbox-plugin-dns'
    },
    'netbox_secrets': {
        'url': 'https://github.com/Onemind-Services-LLC/netbox-secrets',
        'dir': 'netbox-secrets',
        'pip': 'netbox-secrets'
    },
    'netbox_qrcode': {
        'url': 'https://github.com/netbox-community/netbox-qrcode',
        'dir': 'netbox-qrcode',
        'pip': 'netbox-qrcode'
    },
    'netbox_ipcalculator': {
        'url': 'https://github.com/PieterL75/netbox_ipcalculator',
        'dir': 'netbox_ipcalculator',
        'pip': 'netbox-ipcalculator'
    },
    'phonebox_plugin': {
        'url': 'https://github.com/iDebugAll/phonebox_plugin',
        'dir': 'phonebox_plugin',
        'pip': 'phonebox-plugin'         
    },
    'validity': {
        'url': 'https://github.com/amyasnikov/validity',
        'dir': 'validity',
        'pip': 'netbox-validity'           
    },
    'netbox_reorder_rack': {
        'url': 'https://github.com/netbox-community/netbox-reorder-rack',
        'dir': 'netbox-reorder-rack',
        'pip': 'netbox-reorder-rack'            
    }

}
    

print("\n\n##### Plugin dev environment (mebbes, if you use git) builder #####\n")

print ("# Please Enter the NetBox version (note: beta releases not supported)")

i_version="beta"
t = version_match.match(i_version)
while not t:
    i_version = input("< Netbox Version (eg: v4.1.1): ")
    t = version_match.match(i_version)

if i_version.startswith("v4.1"):
    i_branching = input("< Branching Support (y/n): ").lower()
else:
    i_branching = "0"

if i_branching == "y":
    i_branching = 1
else:
    i_branching = 0

for name in PLUGINS.keys():
    print(name)

print("\n")
i_plugin_name = "wibble"
while i_plugin_name not in PLUGINS.keys():
    i_plugin_name = input("< Enter Plugin Name: ")

i_method="v"
while i_method not in ["g","p"]:
    i_method = input("< Install via git, or pip ? (g/p): ").lower()


if os.path.isdir(f"{PLUGINS[i_plugin_name]['dir']}"):
    os.system(f"rm -rf {PLUGINS[i_plugin_name]['dir']}")

if i_method=="g":
    print("## CLONING REPO ...")
    os.system(f"git clone {PLUGINS[i_plugin_name]['url']}")
else:
    os.system(f"mkdir {PLUGINS[i_plugin_name]['dir']}")

print("* Building Dev Environment \n")
new_dir = f"{PLUGINS[i_plugin_name]['dir']}/develop_{i_plugin_name}"
os.system(f"mkdir {new_dir}")

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("Dockerfile.j2")
content = template.render(
    netbox_branching=i_branching,
    netbox_version=i_version,
    install_method=i_method,
    netbox_plugin=PLUGINS[i_plugin_name]['pip']
)
with open(f"{new_dir}/Dockerfile", mode="w", encoding="utf-8") as message:
        message.write(content)

template = environment.get_template("configuration.py.j2")
content = template.render(
    netbox_branching=i_branching,
    netbox_plugin=i_plugin_name
)
with open(f"{new_dir}/configuration.py", mode="w", encoding="utf-8") as message:
        message.write(content)

os.system(f"cp templates/dev.env {new_dir}/dev.env")
if i_branching:
    os.system(f"cp templates/local_settings.py {new_dir}/local_settings.py")
template = environment.get_template("docker-compose.yml.j2")
content = template.render(
    netbox_branching=i_branching,
    netbox_plugin=i_plugin_name,
    new_dir=f"develop_{i_plugin_name}"
)

with open(f"{new_dir}/docker-compose.yml", mode="w", encoding="utf-8") as message:
        message.write(content)


print("\n# Generation Complete\n")

print("# Please now run the following to bring up the instance on http://localhost:8000 - note do not use -d as this method allows you to watch the build")

print(f" cd {new_dir}")
print(f" docker compose build --no-cache")
print(f" docker compose up")
print("\n Then spawn a new terminal: ")
print(f" superuser set: docker exec -it develop_{i_plugin_name}-netbox-1 /opt/netbox/netbox/manage.py createsuperuser")




