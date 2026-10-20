
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Concessionária - Vendas",
    page_icon="🚗",
    layout="wide"
)

# Catálogo de veículos
CATALOGO = {
    "Fiat Argo": {
        "marca": "Fiat",
        "ano": 2025,
        "preco": 85000.00
    },
    "Chevrolet Onix": {
        "marca": "Chevrolet",
        "ano": 2025,
        "preco": 92000.00
    },
    "Volkswagen Polo": {
        "marca": "Volkswagen",
        "ano": 2025,
        "preco": 98000.00
    },
    "Hyundai HB20": {
        "marca": "Hyundai",
        "ano": 2025,
        "preco": 90000.00
    },
    "Toyota Corolla": {
        "marca": "Toyota",
        "ano": 2025,
        "preco": 165000.00
    },
    "Honda Civic": {
        "marca": "Honda",
        "ano": 2024,
        "preco": 180000.00
    },
    "Jeep Compass": {
        "marca": "Jeep",
        "ano": 2025,
        "preco": 190000.00
    },
    "BYD Dolphin": {
        "marca": "BYD",
        "ano": 2025,
        "preco": 150000.00
    }
}


if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "vendas" not in st.session_state:
    st.session_state.vendas = []


st.title("🚗 Dashboard de Vendas - Concessionária")
st.markdown("---")


total_vendido = sum(
    venda["Total (R$)"] for venda in st.session_state.vendas
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Veículos no catálogo",
        len(CATALOGO)
    )

with col2:
    st.metric(
        "Vendas realizadas",
        len(st.session_state.vendas)
    )

with col3:
    st.metric(
        "Faturamento total",
        f"R$ {total_vendido:,.2f}"
    )

st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")



with col1:
    st.subheader("Seleção de Veículos")

    with st.form("form_veiculo"):
        carro_nome = st.selectbox(
            "Escolha o veículo",
            list(CATALOGO.keys())
        )

        carro = CATALOGO[carro_nome]

        st.write(f"**Marca:** {carro['marca']}")
        st.write(f"**Ano:** {carro['ano']}")
        st.caption(
            f"Preço unitário: R$ {carro['preco']:,.2f}"
        )

        quantidade = st.number_input(
            "Quantidade de veículos",
            min_value=1,
            value=1,
            step=1
        )

        btn_adicionar = st.form_submit_button(
            "Adicionar ao Carrinho",
            use_container_width=True
        )

        if btn_adicionar:
            subtotal = carro["preco"] * quantidade

            st.session_state.carrinho.append({
                "Veículo": carro_nome,
                "Marca": carro["marca"],
                "Ano": carro["ano"],
                "Preço Unit. (R$)": carro["preco"],
                "Qtd": quantidade,
                "Subtotal (R$)": subtotal
            })

            st.success(
                f"{quantidade} unidade(s) de {carro_nome} "
                "adicionada(s) com sucesso!"
            )

    st.subheader("Carrinho de Vendas")

    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(
            st.session_state.carrinho
        )

        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Unit. (R$)": st.column_config.NumberColumn(
                    "Preço Unitário",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )

        if st.button(
            "Limpar Carrinho",
            use_container_width=True
        ):
            st.session_state.carrinho = []
            st.rerun()

    else:
        st.info(
            "O carrinho está vazio. Adicione veículos acima."
        )


with col2:
    st.subheader("Pagamento e Fechamento")

    total_compra = sum(
        item["Subtotal (R$)"]
        for item in st.session_state.carrinho
    )

    st.metric(
        label="TOTAL DA VENDA",
        value=f"R$ {total_compra:,.2f}"
    )

    st.markdown("---")

    valor_recebido = st.number_input(
        "Valor recebido do cliente (R$)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )

    if total_compra == 0:
        st.warning(
            "Adicione veículos ao carrinho antes de realizar "
            "o pagamento."
        )

    else:
        troco = valor_recebido - total_compra

        if valor_recebido == 0:
            st.info("Aguardando o pagamento do cliente.")

        elif valor_recebido < total_compra:
            falta = total_compra - valor_recebido

            st.error(
                f"Valor insuficiente! Faltam "
                f"R$ {falta:,.2f} para concluir a venda."
            )

        else:
            st.success("Pagamento disponível para finalização!")

            st.metric(
                label="TROCO A DEVOLVER",
                value=f"R$ {troco:,.2f}"
            )

            with st.expander("Ver Comprovante da Venda"):
                st.write(
                    f"**Veículos diferentes:** "
                    f"{len(st.session_state.carrinho)}"
                )

                total_unidades = sum(
                    item["Qtd"]
                    for item in st.session_state.carrinho
                )

                st.write(
                    f"**Quantidade de veículos:** {total_unidades}"
                )
                st.write(f"**Total da venda:** R$ {total_compra:,.2f}")
                st.write(f"**Valor recebido:** R$ {valor_recebido:,.2f}")
                st.write(f"**Troco:** R$ {troco:,.2f}")

            if st.button(
                "Finalizar Venda",
                type="primary",
                use_container_width=True
            ):
                st.session_state.vendas.append({
                    "Veículos": ", ".join(
                        item["Veículo"]
                        for item in st.session_state.carrinho
                    ),
                    "Quantidade": sum(
                        item["Qtd"]
                        for item in st.session_state.carrinho
                    ),
                    "Total (R$)": total_compra,
                    "Valor Recebido (R$)": valor_recebido,
                    "Troco (R$)": troco
                })

                st.session_state.carrinho = []
                st.success("Venda finalizada com sucesso!")
                st.rerun()



st.markdown("---")
st.subheader("Histórico de Vendas")

if st.session_state.vendas:
    df_vendas = pd.DataFrame(st.session_state.vendas)

    st.dataframe(
        df_vendas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total (R$)": st.column_config.NumberColumn(
                "Total da Venda",
                format="R$ %.2f"
            ),
            "Valor Recebido (R$)": st.column_config.NumberColumn(
                "Valor Recebido",
                format="R$ %.2f"
            ),
            "Troco (R$)": st.column_config.NumberColumn(
                "Troco",
                format="R$ %.2f"
            )
        }
    )

else:
    st.info("Nenhuma venda foi realizada nesta sessão.")
