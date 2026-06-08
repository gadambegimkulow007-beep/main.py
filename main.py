import random
import os
import socket
import threading

class EmptyColor:
    def __getattr__(self, name): return ""
Fore = EmptyColor()
Style = EmptyColor()

def pass_maglumatyny_oky():
    if os.path.exists("pass_data.txt"):
        with open("pass_data.txt", "r") as f:
            maglumat = f.read().strip().split(",")
            if len(maglumat) == 2:
                return int(maglumat[0]), int(maglumat[1])
    return 1, 0

def pass_maglumatyny_yaz(tier, xp):
    with open("pass_data.txt", "w") as f:
        f.write(f"{tier},{xp}")

def xp_gos(gazanylan_xp):
    tier, xp = pass_maglumatyny_oky()
    xp += gazanylan_xp
    print(f"✨ +{gazanylan_xp} XP gazandyňyz!")
    while xp >= 100:
        xp -= 100
        tier += 1
        print(f"🔥 GONG! TIER BÖKDIŇIZ! Täze dereje: Tier {tier} 🎉")
    pass_maglumatyny_yaz(tier, xp)

def pass_status_gorkez():
    tier, xp = pass_maglumatyny_oky()
    print(f"\n--- SEASON 1 PASS STATUSY ---")
    print(f"Häzirki Dereje: Tier {tier}")
    print(f"XP Progress: [{xp}/100]")
    bar = "█" * (xp // 10) + "-" * (10 - (xp // 10))
    print(f"[{bar}]")

def rekordy_oky():
    if os.path.exists("rekord.txt"):
        with open("rekord.txt", "r") as f:
            return int(f.read().strip())
    return 999

def rekordy_yaz(taze_rekord):
    with open("rekord.txt", "w") as f:
        f.write(str(taze_rekord))

def sany_tap_oyny(nickname):
    print("\n" + "="*40)
    print(f"===   SANY TAP OÝNY | Oýunçy: {nickname}   ===")
    print("="*40)
    iň_gowy_rekord = rekordy_oky()
    if iň_gowy_rekord != 999:
        print(f"🏆 Häzirki rekord: {iň_gowy_rekord} synanyşyk")
    gizlin_san = random.randint(1, 100)
    jan_sany = 7
    synanyshyk = 0
    while jan_sany > 0:
        print(f"Galan jan: " + "❤️ " * jan_sany)
        try:
            tahmynyňyz = int(input("Tahmynyňyzy ýazyň: "))
        except ValueError:
            print("🛑 Diňe san giriziň!\n")
            continue
        synanyshyk += 1
        jan_sany -= 1
        if tahmynyňyz < gizlin_san:
            print("Has uly san aýdyň! ⬆️\n")
        elif tahmynyňyz > gizlin_san:
            print("Has kiçi san aýdyň! ⬇️\n")
        else:
            print(f"\n🎉 Gutlaýarys {nickname}! Sany {synanyshyk} synanyşykda tapdyňyz!")
            xp_gos(40)
            if synanyshyk < iň_gowy_rekord:
                print(f"🔥 TÄZE REKORD! Ulgama ýazyldy!")
                rekordy_yaz(synanyshyk)
            return
    print(f"\n💀 Janyňyz gutardy! Gizlin san: {gizlin_san}")
    xp_gos(10)

def xabarlary_al(client_socket):
    while True:
        try:
            xabar = client_socket.recv(1024).decode('utf-8')
            if not xabar: break
            print(xabar)
        except:
            break

def multiplayer_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(1)
    print("\n[Ulgam] Hotspot Server başladyldy! Port: 5555")
    print("Dostuňyzyň birikmegine garaşylýar...")
    conn, addr = server.accept()
    print(f"\n🎉 Dostuňyz birikdi! (IP: {addr})")
    threading.Thread(target=xabarlary_al, args=(conn,), daemon=True).start()
    while True:
        mesaj = input()
        if mesaj.lower() == 'exit':
            conn.close()
            break
        try:
            conn.send(f"\n[Dostuňyz]: {mesaj}".encode('utf-8'))
        except:
            break
    server.close()

def multiplayer_client():
    server_ip = input("Dostuňyzyň IP adresini giriziň: ").strip()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, 5555))
        print("🎉 Servere üstünlikli birikdiňiz!")
    except Exception as e:
        print(f"🛑 Birigip bolmady! {e}")
        return
    threading.Thread(target=xabarlary_al, args=(client,), daemon=True).start()
    while True:
        mesaj = input()
        if mesaj.lower() == 'exit':
            client.close()
            break
        try:
            client.send(f"\n[Dostuňyz]: {mesaj}".encode('utf-8'))
        except:
            break

def esasy_menu():
    print("=== TERMUX MULTIPLAYER PRO PORTAL ===")
    nickname = input("Oýunçy adyňyz (Nickname): ").strip()
    if not nickname: nickname = "Oýunçy"
    while True:
        print("\n" + "="*35)
        print(f"Salam, {nickname}! Esasy Menýu:")
        print("1. Sany Tap Oýny (Solo + XP) 🔢")
        print("2. Hotspot: Çat we Oýun Başlat (SERVER) 🛠️")
        print("3. Hotspot: Dostuňyza Goşul (CLIENT) 🔌")
        print("4. Season Pass Statusyny Gör 🏆")
        print("5. Çykyş 🚪")
        print("="*35)
        saylaw = input("Saýlawyňyz (1-5): ").strip()
        if saylaw == "1":
            sany_tap_oyny(nickname)
        elif saylaw == "2":
            multiplayer_server()
        elif saylaw == "3":
            multiplayer_client()
        elif saylaw == "4":
            pass_status_gorkez()
        elif saylaw == "5":
            break

if __name__ == "__main__":
    esasy_menu()
