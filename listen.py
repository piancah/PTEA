import subprocess
import time
import smtplib
import json

config = json.loads(open("listen.json","r",encoding="utf-8").read())
watchlist = config["watchlist"]
email = config["sender"]
password = config["senderpw"]
to = config["reciever"]
interval = config["interval_seconds"]
def get_python_process():
   try:
      # Run the shell command to get the list of Python processes
      result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True)
      output = result.stdout

      # Extract and return the process names
      process_names = [line.split()[-1] for line in output.splitlines() if 'python' in line]
      return process_names
   except Exception as e:
      print(f"Error: {e}")
      return []



def main():
   initial_processes = watchlist
   print("Checker started")
   
   while True:
      print(f"running checker in next {interval} seconds")
	  time.sleep(interval)

      current_processes = get_python_process()
      unknown_processes = list(set(current_processes) - set(initial_processes))
      known_processes = list(set(current_processes) - set(unknown_processes))
      missing_processes = list(set(initial_processes) - set(known_processes))

      if len(missing_processes) > 0:
		 print(f"Connector(s) {missing_processes} is down")
		 try:
			with smtplib.SMTP_SSL(config["emailserverip"], 465) as smtp:

				smtp.login(email, password)

				subject = f"{missing_processes} is down"
				body = f"Connector(s) {missing_processes} is down"

				msg = "Subject: {}\n\n{}".format(subject, body)

				smtp.sendmail(email, to, msg)

				print("Connector down")
				print("Email sent")

		 except Exception as e:
			print(e)
			print("Email not sent")
		 else:
			print("No connectors down..")
			
if __name__ == "__main__":
   main()



