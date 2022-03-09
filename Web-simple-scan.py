#coding:utf-8
import socket
from whois import whois
import requests

url = str(input("Please input URL: "))
print("Start scanning...")
ip = socket.gethostbyname(url)
WebWhois = whois(url)
r = requests.get("http://" + url)
MiddlewareServer = r.headers["Server"]
print("Web message:")
print(f"Web's IP: {ip}")
print(f"Web's middleware: {MiddlewareServer}")
print(f"Web's whois:\n{WebWhois}")
