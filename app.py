from flask import Flask, request, render_template
import re

app = Flask(__name__)



def ipclassification(ip):
    ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not ip_regex.match(ip):
        return "Invalid IP Address"

    octets = ip.split(".")
    octets = [int(octet) for octet in octets]

    if octets[0] >= 1 and octets[0] <= 127:
        ip_class = "A"
        if octets[0] == 10:
            ip_type = "Private"
        elif octets[0] == 127:
            ip_type = "Loopback"
        else:
            ip_type = "Public"
        subnet_mask = "255.0.0.0"
        network_address = f"{octets[0]}.0.0.0"
        first_ip_address = f"{octets[0]}.0.0.1"
        last_ip_address = f"{octets[0]}.255.255.254"
        broadcast_address = f"{octets[0]}.255.255.255"
        host_address_range = f"{octets[0]}.0.0.1 - {octets[0]}.255.255.254"
    elif octets[0] >= 128 and octets[0] <= 191:
        ip_class = "B"
        if octets[0] == 172:
            ip_type = "Private"
        else:
            ip_type = "Public"
        subnet_mask = "255.255.0.0"
        network_address = f"{octets[0]}.{octets[1]}.0.0"
        first_ip_address = f"{octets[0]}.{octets[1]}.0.1"
        last_ip_address = f"{octets[0]}.{octets[1]}.255.254"
        broadcast_address = f"{octets[0]}.{octets[1]}.255.255"
        host_address_range = f"{octets[0]}.{octets[1]}.0.1 - {octets[0]}.{octets[1]}.255.254"
    elif octets[0] >= 192 and octets[0] <= 223:
        ip_class = "C"
        if octets[0] == 192:
            ip_type = "Private"
        else:
            ip_type = "Public"
        subnet_mask = "255.255.255.0"
        network_address = f"{octets[0]}.{octets[1]}.{octets[2]}.0"
        first_ip_address = f"{octets[0]}.{octets[1]}.{octets[2]}.1"
        last_ip_address = f"{octets[0]}.{octets[1]}.{octets[2]}.254"
        broadcast_address = f"{octets[0]}.{octets[1]}.{octets[2]}.255"
        host_address_range = f"{octets[0]}.{octets[1]}.{octets[2]}.1 - {octets[0]}.{octets[1]}.{octets[2]}.254"
    elif octets[0] >= 224 and octets[0] <= 239:
        ip_class = "D"
        ip_type = "Reserved"
        subnet_mask = "N/A"
        network_address = "N/A"
        first_ip_address = "N/A"
        last_ip_address = "N/A"
        broadcast_address = "N/A"
        host_address_range = "N/A"
    elif octets[0] >= 240 and octets[0] <= 255:
        ip_class = "E"
        ip_type = "Reserved"
        subnet_mask = "N/A"
        network_address = "N/A"
        first_ip_address = "N/A"
        last_ip_address = "N/A"
        broadcast_address = "N/A"
        host_address_range = "N/A"

    return {
        "IP Class": ip_class,
        "IP Type": ip_type,
        "Subnet Mask": subnet_mask,
        "Network Address": network_address,
        "First IP Address": first_ip_address,
        "Last IP Address": last_ip_address,
        "Broadcast Address": broadcast_address,
        "Host Address Range": host_address_range
    }
def Shorting_ipv6(ip):
      octets = ip.split(":")
      
      for i in range(len(octets)):
            if octets[i] != "":
                  octets[i] = octets[i].lstrip('0')
                  if octets[i] == "":
                        octets[i] = "0"
      
      ip = ":".join(octets)
      
      if "::" not in ip:
            while ":::" in ip:
                  ip = ip.replace(":::", "::")
      
      parts = ip.split(":")
      longest_zero_sequence = []
      current_sequence = []
      
      for i in range(len(parts)):
            if parts[i] == "0":
                  current_sequence.append(i)
            else:
                  if len(current_sequence) > len(longest_zero_sequence):
                        longest_zero_sequence = current_sequence
                  current_sequence = []
      
      if len(current_sequence) > len(longest_zero_sequence):
            longest_zero_sequence = current_sequence
      
      if len(longest_zero_sequence) > 1:
            start = longest_zero_sequence[0]
            end = longest_zero_sequence[-1] + 1
            ip = ":".join(parts[:start]) + "::" + ":".join(parts[end:])
            if ip.startswith(":"):
                  ip = ":" + ip
            if ip.endswith(":"):
                  ip = ip + ":"

      return ip

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")
@app.route("/ipv4", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ip_address = request.form["ip_address"]
        ip_info = ipclassification(ip_address)
        return render_template("ipv4.html", ip_info=ip_info, ip_address=ip_address)
    return render_template("ipv4.html")
@app.route("/ipv6", methods=["GET", "POST"])
def index1():
    if request.method == "POST":
        ip_address = request.form["ip_address"]
        ip_info = Shorting_ipv6(ip_address)
        return render_template("ipv6.html", ip_info=ip_info, ip_address=ip_address)
    return render_template("ipv6.html")

if __name__ == "__main__":
    app.run(debug=True)
