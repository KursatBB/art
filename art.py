import smtplib

def relay_test(sender_email, receiver_email, smtp_server, test_description, smtp_port=25):
    server = None
    try:
        # SMTP sunucusuna bağlan
        server = smtplib.SMTP(smtp_server, smtp_port)
        #server.set_debuglevel(1)  # Telnet benzeri çıktı için debug seviyesi ayarlanıyor
        server.ehlo()

        # MAIL FROM komutunu gönder
        server.mail(sender_email)
        
        # RCPT TO komutunu gönder ve yanıtı kontrol et
        code, response = server.rcpt(receiver_email)
        if code != 250:
            print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: Alıcı mail reddedildi - {response.decode('utf-8')}")
            return  # Hata varsa veri göndermeden bağlantıyı sonlandır
        
        # DATA komutunu gönder
        message = (
            f"Subject: Relay Test\r\n"
            f"\r\n"
            f"This is a test message\r\n"
            f".\r\n"  # Mesaj sonu: SMTP'de "." ile bitirilir, "\r\n" ile sonlandırılır
        )
        code, response = server.data(message.encode('utf-8'))  # Mesajı UTF-8 olarak encode et ve yanıtı kontrol et

        if code == 250:
            print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarılı")
        else:
            print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: {response.decode('utf-8')}")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: Alıcı mail reddedildi - {e}")
    except smtplib.SMTPDataError as e:
        print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: Veri gönderimi hatası - {e}")
    except smtplib.SMTPServerDisconnected as e:
        print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: Sunucu bağlantısı beklenmedik şekilde kapandı - {e}")
    except Exception as e:
        # Diğer hatalar durumunda sonucu yazdır
        print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: {e}")
    finally:
        if server:
            try:
                # Bağlantının hala aktif olup olmadığını kontrol et
                if server.sock:
                    server.quit()
            except smtplib.SMTPServerDisconnected:
                # Eğer sunucu zaten kapatılmışsa sadece bağlantıyı serbest bırak
                server.close()

if __name__ == "__main__":
    # Kullanıcıdan gerekli mail adreslerini al
    sender_email = input("Dışarda geçerli olan ilk mail adresini girin: ")
    sender_email2 = "kektest@yopmail.com"  # Sabit dış mail adresi
    invalid_external_email = "belkikektek@tekkeksitekoverflow.com"  # Sabit dış geçersiz mail adresi
    internal_valid_email = input("İçerde geçerli olan mail adresini girin: ")
    internal_invalid_email = input("İçerde geçersiz olan mail adresini girin: ")
    smtp_server = input("SMTP sunucusunun IP adresini veya domain adını girin: ")

    # Test 0: Dışarda geçerli olan mailden > dışarda geçerli olan mailde
    relay_test(sender_email, sender_email2, smtp_server, "Dışarda geçerli olandan dışarda geçerli olana")
    
    # Test 1: Dışarda geçerli olan mailden > dışarda geçersiz olan maile
    relay_test(sender_email, invalid_external_email, smtp_server, "Dışarda geçerli olandan dışarda geçersiz olana")

    # Test 2: Dışarda geçerli olan mailden > içerde geçerli olan maile
    relay_test(sender_email, internal_valid_email, smtp_server, "Dışarda geçerli olandan içerde geçerli olana")

    # Test 3: Dışarda geçerli olan mailden > içerde geçersiz olan maile
    relay_test(sender_email, internal_invalid_email, smtp_server, "Dışarda geçerli olandan içerde geçersiz olana")

    # Test 4: Dışarda geçersiz olan mailden > dışarda geçerli olan maile
    relay_test(invalid_external_email, sender_email2, smtp_server, "Dışarda geçersiz olandan dışarda geçerli olana")

    # Test 5: Dışarda geçersiz olan mailden > dışarda geçersiz olan maile
    relay_test(invalid_external_email, invalid_external_email, smtp_server, "Dışarda geçersiz olandan dışarda geçersiz olana")

    # Test 6: Dışarda geçersiz olan mailden > içerde geçerli olan maile
    relay_test(invalid_external_email, internal_valid_email, smtp_server, "Dışarda geçersiz olandan içerde geçerli olana")

    # Test 7: Dışarda geçersiz olan mailden > içerde geçersiz olan maile
    relay_test(invalid_external_email, internal_invalid_email, smtp_server, "Dışarda geçersiz olandan içerde geçersiz olana")

    # Test 8: İçerde geçerli olan mailden > içerde geçerli olan maile
    relay_test(internal_valid_email, internal_valid_email, smtp_server, "İçerde geçerli olandan içerde geçerli olana")

    # Test 9: İçerde geçerli olan mailden > içerde geçersiz olan maile
    relay_test(internal_valid_email, internal_invalid_email, smtp_server, "İçerde geçerli olandan içerde geçersiz olana")

    # Test 10: İçerde geçerli olan mailden > dışarda geçerli olan maile
    relay_test(internal_valid_email, sender_email2, smtp_server, "İçerde geçerli olandan dışarda geçerli olana")

    # Test 11: İçerde geçerli olan mailden > dışarda geçersiz olan maile
    relay_test(internal_valid_email, invalid_external_email, smtp_server, "İçerde geçerli olandan dışarda geçersiz olana")

    # Test 12: İçerde geçersiz olan mailden > içerde geçerli olan maile
    relay_test(internal_invalid_email, internal_valid_email, smtp_server, "İçerde geçersiz olandan içerde geçerli olana")

    # Test 13: İçerde geçersiz olan mailden > içerde geçersiz olan maile
    relay_test(internal_invalid_email, internal_invalid_email, smtp_server, "İçerde geçersiz olandan içerde geçersiz olana")

    # Test 14: İçerde geçersiz olan mailden > dışarda geçerli olan maile
    relay_test(internal_invalid_email, sender_email2, smtp_server, "İçerde geçersiz olandan dışarda geçerli olana")

    # Test 15: İçerde geçersiz olan mailden > dışarda geçersiz olan maile
    relay_test(internal_invalid_email, invalid_external_email, smtp_server, "İçerde geçersiz olandan dışarda geçersiz olana")
