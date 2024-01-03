import subprocess
import time
import smtplib

watchlist = ['temporary.py' , "temp.py", "whatever.py"]
email = "opencti@testmail.local"
password = "roundcubeP@55w0rd"
to = ["socuser@testmail.local"]
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

   while True:
      time.sleep(5)

      current_processes = get_python_process()
      unknown_processes = list(set(current_processes) - set(initial_processes))
      known_processes = list(set(current_processes) - set(unknown_processes))
      missing_processes = list(set(initial_processes) - set(known_processes))

      if len(missing_processes) > 0:
         with smtplib.SMTP_SSL('192.168.191.57', 465) as smtp:

            smtp.login(email, password)

            subject = "Connector Down"
            body = f"Connector(s) {missing_processes} is down"

            msg = "Subject: {}\n\n{}".format(subject, body)

            smtp.sendmail(email, to, msg)

         print("Connector down")
         print("Email sent")

if __name__ == "__main__":
   main()



