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
