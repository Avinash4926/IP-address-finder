from flask import Flask, render_template, request
import socket
import requests

app = Flask(__name__)

def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()

        if data["status"] == "success":
            return {
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp")
            }
    except:
        pass

    return None

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None

    if request.method == "POST":
        domain = request.form.get("domain")

        try:
            _, _, ip_list = socket.gethostbyname_ex(domain)

            for ip in ip_list:
                location = get_ip_location(ip)
                results.append({
                    "ip": ip,
                    "location": location
                })

        except socket.gaierror:
            error = "Invalid domain name or DNS error"

    return render_template(
        "index.html",
        results=results,
        error=error,
        http_port=80,
        https_port=443
    )

if __name__ == "__main__":
    app.run(debug=True)
