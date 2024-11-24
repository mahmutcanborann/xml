import streamlit as st
import requests
import xml.etree.ElementTree as et


def fetch_sitemap_links(url):
    """
    Verilen URL'deki sitemap veya alt sitemap dosyalarını işler ve tüm URL'leri döner.
    """
    urls = []
    response = requests.get(url)

    if response.status_code == 200:
        veri = response.text
        if veri.strip().startswith("<") and veri.strip().endswith(">"):  # Temel XML kontrolü
            linkler = et.fromstring(veri)
            for link in linkler:
                if link.tag.endswith("sitemap"):  # Alt sitemap durumunu kontrol et
                    for child in link:
                        if child.tag.endswith("loc"):  # Alt sitemap'ın URL'sini al
                            alt_sitemap_url = child.text
                            urls.extend(fetch_sitemap_links(alt_sitemap_url))  # Alt sitemap'ı işle
                elif link.tag.endswith("url"):  # Normal URL'leri al
                    for child in link:
                        if child.tag.endswith("loc"):  # URL'yi al
                            urls.append(child.text)
    return urls


# Streamlit uygulaması
url = st.text_input('Sitemap URL giriniz')
btn = st.button("Getir")

if btn and url:  # Buton tıklanmış ve URL girilmişse
    if not url.startswith("http://") and not url.startswith("https://"):
        st.error("Geçerli bir URL giriniz (http:// veya https:// ile başlamalı).")
    else:
        all_links = fetch_sitemap_links(url)  # Tüm URL'leri al
        if all_links:
            for link in all_links:
                st.write(link)  # Her bir URL'yi ekrana yazdır
        else:
            st.warning("Hiçbir bağlantı bulunamadı.")
else:
    st.info("Lütfen bir URL girin ve butona basın.")
