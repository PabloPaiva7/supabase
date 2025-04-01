import streamlit as st
from supabase import create_client

# Configuração do Supabase
SUPABASE_URL = "https://gjfydabmcvfdklhujdqy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdqZnlkYWJtY3ZmZGtsaHVqZHF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM1MTU2ODUsImV4cCI6MjA1OTA5MTY4NX0.RII1C4w6yx4UMpSg8ELlC3kdwZEedgacEk29jbMkVA4"  # Substitua pela chave real
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Gerenciamento de Desempenho de Colaboradores")

# Buscar e exibir dados da tabela
st.subheader("Dados de desempenho dos colaboradores")
response = supabase.table("desempenho_colaboradores").select("*").limit(5).execute()

if response.data:
    st.table(response.data)
else:
    st.write("Nenhum dado encontrado.")

# Formulário para inserir novos dados
st.subheader("Registrar Desempenho")
with st.form("form_registro"):
    colaborador_id = st.text_input("ID do Colaborador")
    nome_colaborador = st.text_input("Nome do Colaborador")
    total_demandas = st.number_input("Total de Demandas", min_value=0)
    demandas_concluidas = st.number_input("Demandas Concluídas", min_value=0)
    demandas_devolvidas = st.number_input("Demandas Devolvidas", min_value=0)
    taxa_conclusao = (demandas_concluidas / total_demandas * 100) if total_demandas > 0 else 0
    submit = st.form_submit_button("Registrar")

    if submit:
        try:
            data = {
                "colaborador_id": colaborador_id,
                "nome_colaborador": nome_colaborador,
                "total_demandas": total_demandas,
                "demandas_concluidas": demandas_concluidas,
                "taxa_conclusao": taxa_conclusao,
                "demandas_devolvidas": demandas_devolvidas
            }
            response = supabase.table("desempenho_colaboradores").insert(data).execute()
            st.success("Registro inserido com sucesso!")
        except Exception as e:
            st.error(f"Erro ao inserir dados: {e}")

    