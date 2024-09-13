import os
from jinja2 import Environment, FileSystemLoader



PLUGINS = {
    'netbox_bgp': {
        'url':  'https://github.com/netbox-community/netbox-bgp',
        'dir':  'netbox-bgp'
    },
    'netbox_acls': {
        'url':  'https://github.com/netbox-community/netbox-acls',
        'dir':  'netbox-acls'
    },
    'netbox_topology_views': {
        'url':  'https://github.com/netbox-community/netbox-topology-views',
        'dir':  'netbox-topology-views'
    }
    'netbox_inventory': {
         'url': 'https://github.com/ArnesSI/netbox-inventory',
         'dir': 'netbox-inventory'
    }
}

print("\n\n##### Plugin dev environment builder #####\n")
i_version = input("Netbox Version (eg: v4.1.1): ")
if i_version.startswith("v4.1"):
    i_branching = input("Branching Support (y/n): ").lower()
else:
    i_branching = "0"

if i_branching == "y":
    i_branching = 1
else:
    i_branching = 0

for name in PLUGINS.keys():
    print(name)
i_plugin_name = "wibble"
while i_plugin_name not in PLUGINS.keys():
    i_plugin_name = input("Enter Plugin Name: ")

print("## CLONING REPO ...")
if os.path.isdir(f"{PLUGINS[i_plugin_name]['dir']}"):
    os.system(f"rm -rf {PLUGINS[i_plugin_name]['dir']}")

os.system(f"git clone {PLUGINS[i_plugin_name]['url']}")
print("* Building Dev Environment \n")
new_dir = f"{PLUGINS[i_plugin_name]['dir']}/develop_{i_plugin_name}"
os.system(f"mkdir {new_dir}")

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("Dockerfile.j2")
content = template.render(
    netbox_branching=i_branching,
    netbox_version=i_version
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


print("\nNow:\'n\n")
print(f" cd {new_dir}")
print(f" docker compose build --no-cache")
print(f" docker compose up")
print(f" superuser set: docker exec -it develop_{i_plugin_name}-netbox-1 /opt/netbox/netbox/manage.py createsuperuser")

print("\nPlugin is installed in editable mode\n")



