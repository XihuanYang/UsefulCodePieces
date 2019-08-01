uthor: Xihuan Yang
## This script is used to start tcpdump on all interfaces
## script will exited when monitor end file in ./dump_files
## all the .cap file will be saved in ./dump_files
###################################################################################################

import os
import subprocess

EMPTY_STRING = ""

dump_path = './dump_files'
if not os.path.exists(dump_path):
    os.mkdir(dump_path)

cmd = "ip -o link | awk '{if($2 ~ /^[eth|xenbr|vif]/) print $2,$(NF-2)}'"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
std_out, std_err = p.communicate()

ifaces_macs = []
if std_out != EMPTY_STRING:
    for iface_mac in std_out.splitlines():
        ifaces_macs.append(iface_mac)
elif std_err != EMPTY_STRING:
    print "Command execute return error output:"
    print std_err
else:
    print "Command execute returns empty output."

proc_running = []
for iface_mac in ifaces_macs:
    iface_mac_list = iface_mac.split(": ")
    iface = iface_mac_list[0]
    mac = iface_mac_list[1].replace(":", "_")
    tcpdump_file = "./dump_files/" + iface + "_" + mac + ".cap"
    tcpdump_command = ["sudo tcpdump", "-i", iface, "-s0", "-w", tcpdump_file]
    tcpdump_process = subprocess.Popen(tcpdump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_running.append(tcpdump_process)
    print iface_mac

while True:
   if os.path.exists("./dump_files/end"):
       break

for proc in proc_running:
    proc.kill()

