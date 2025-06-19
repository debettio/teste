
import streamlit as st
import fitz  # PyMuPDF
import re
import io

st.set_page_config(page_title="Grifador de PDF Jurídico", layout="centered")

st.title("📚 Grifador de PDF Jurídico por IA")
st.markdown("Envie um PDF e receba o arquivo com grifos automáticos aplicados com base em regras jurídicas personalizadas.")

uploaded_file = st.file_uploader("📤 Envie seu PDF", type="pdf")

highlight_rules = [
    {"pattern": r"^\d+\..*", "color": (1, 0, 0)},  # Título - Vermelho
    {"pattern": r"^[a-zA-Z]\..*", "color": (0.5, 0.5, 0.5)},  # Subtítulo - Cinza
    {"pattern": r"\b(conceito|define-se|entende-se)\b", "color": (1, 1, 0)},  # Conceito - Amarelo
    {"pattern": r"\b(pressuposto|fundamento|baseado em)\b", "color": (0.2, 0.4, 1)},  # Conceito paralelo - Azul
    {"pattern": r"\b(STF|súmula vinculante|s\\.v\\.)\b", "color": (0.4, 0.8, 1)},  # STF - Azul piscina
    {"pattern": r"\b(STJ|súmula n[ºo]\\.|jurisprudência do STJ)\b", "color": (0.7, 0.4, 1)},  # STJ - Lilás
    {"pattern": r"\b(ex:|por exemplo|exemplo)\b", "color": (1, 0.4, 0.7)},  # Exemplo - Rosa pink
    {"pattern": r"\b(prazo|até \d+ dias?|durante|regra)\b", "color": (1, 0.7, 0.8)},  # Regras/prazos - Rosa bebê
    {"pattern": r"\b(art\\.|lei n[ºo]|código penal|constituição)\b", "color": (1, 0.5, 0)},  # Lei - Laranja
    {"pattern": r"\b(exceto|salvo|não se aplica)\b", "color": (0.7, 1, 0.7)},  # Exceção - Verde claro
    {"pattern": r"\b(diverge|divergência|não há consenso)\b", "color": (0, 0.4, 0)},  # Divergência - Verde escuro
    {"pattern": r"\b(importante|destaca-se|atenção|relevante)\b", "underline": True},  # Sublinhado - Preto
]

def highlight_pdf(input_bytes):
    doc = fitz.open(stream=io.BytesIO(input_bytes), filetype="pdf")
    for page in doc:
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4]
            for rule in highlight_rules:
                if re.search(rule["pattern"], text, re.IGNORECASE):
                    rect = fitz.Rect(b[0], b[1], b[2], b[3])
                    if "color" in rule:
                        highlight = page.add_highlight_annot(rect)
                        highlight.set_colors(stroke=rule["color"])
                        highlight.update()
                    if "underline" in rule:
                        underline = page.add_underline_annot(rect)
                        underline.set_colors(stroke=(0, 0, 0))
                        underline.update()
    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)
    return output

if uploaded_file:
    with st.spinner("Aplicando grifos no PDF..."):
        result_pdf = highlight_pdf(uploaded_file.read())
        st.success("✅ Grifos aplicados com sucesso!")
        st.download_button("📥 Baixar PDF grifado", result_pdf, file_name="saida_marcada.pdf")
