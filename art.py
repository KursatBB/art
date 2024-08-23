import smtplib

def relay_test(sender_email, receiver_email, smtp_server, test_description, smtp_port=25):
    server = None
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()

        server.mail(sender_email)
        code, response = server.rcpt(receiver_email)
        if code != 250:
            print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: Alıcı mail reddedildi - {response.decode('utf-8')}")
            return 
        
        message = (
            f"Subject: Relay Test\r\n"
            f"\r\n"
            f"This is a test message\r\n"
            f".\r\n"
        )
        code, response = server.data(message.encode('utf-8'))

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
        print(f"{test_description} testi gerçekleştirildi. Sonuç: Başarısız\nHata: {e}")
    finally:
        if server:
            try:
                if server.sock:
                    server.quit()
            except smtplib.SMTPServerDisconnected:
                server.close()

if __name__ == "__main__":
    sender_email = input("Dışarda geçerli olan ilk mail adresini girin: ")
    sender_email2 = "kektest@yopmail.com"
    invalid_external_email = "belkikektek@tekkeksitekoverflow.com"
    internal_valid_email = input("İçerde geçerli olan mail adresini girin: ")
    internal_invalid_email = input("İçerde geçersiz olan mail adresini girin: ")
    smtp_server = input("SMTP sunucusunun IP adresini veya domain adını girin: ")

    relay_test(sender_email, sender_email2, smtp_server, "Dışarda geçerli olandan dışarda geçerli olana")
    relay_test(sender_email, invalid_external_email, smtp_server, "Dışarda geçerli olandan dışarda geçersiz olana")
    relay_test(sender_email, internal_valid_email, smtp_server, "Dışarda geçerli olandan içerde geçerli olana")
    relay_test(sender_email, internal_invalid_email, smtp_server, "Dışarda geçerli olandan içerde geçersiz olana")
    relay_test(invalid_external_email, sender_email2, smtp_server, "Dışarda geçersiz olandan dışarda geçerli olana")
    relay_test(invalid_external_email, invalid_external_email, smtp_server, "Dışarda geçersiz olandan dışarda geçersiz olana")
    relay_test(invalid_external_email, internal_valid_email, smtp_server, "Dışarda geçersiz olandan içerde geçerli olana")
    relay_test(invalid_external_email, internal_invalid_email, smtp_server, "Dışarda geçersiz olandan içerde geçersiz olana")
    relay_test(internal_valid_email, internal_valid_email, smtp_server, "İçerde geçerli olandan içerde geçerli olana")
    relay_test(internal_valid_email, internal_invalid_email, smtp_server, "İçerde geçerli olandan içerde geçersiz olana")
    relay_test(internal_valid_email, sender_email2, smtp_server, "İçerde geçerli olandan dışarda geçerli olana")
    relay_test(internal_valid_email, invalid_external_email, smtp_server, "İçerde geçerli olandan dışarda geçersiz olana")
    relay_test(internal_invalid_email, internal_valid_email, smtp_server, "İçerde geçersiz olandan içerde geçerli olana")
    relay_test(internal_invalid_email, internal_invalid_email, smtp_server, "İçerde geçersiz olandan içerde geçersiz olana")
    relay_test(internal_invalid_email, sender_email2, smtp_server, "İçerde geçersiz olandan dışarda geçerli olana")
    relay_test(internal_invalid_email, invalid_external_email, smtp_server, "İçerde geçersiz olandan dışarda geçersiz olana")
