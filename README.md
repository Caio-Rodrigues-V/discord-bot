# 🤖 Bot de Automação para Discord com Integração à Binance API

## 📌 **Descrição**
Este projeto é um bot para Discord desenvolvido em **Python** que utiliza a **API da Binance** para realizar operações relacionadas a criptomoedas.  
O bot permite consultar informações de mercado, gerar gráficos históricos de preços, converter valores entre moedas e até mesmo limpar mensagens no chat.  

---

## 🚀 **Funcionalidades**
- 🔎 **Informações de mercado**: Consulte preços, volume, variação e capitalização de mercado de qualquer moeda listada na Binance.  
- 📈 **Gráficos históricos**: Gere gráficos de preços com dados históricos diretamente no Discord.  
- 💱 **Conversão de moedas**: Converta valores entre pares de moedas suportados.  
- 🧹 **Gerenciamento de chat**: Limpe até 100 mensagens de uma vez em um canal.

---

## 🛠️ **Tecnologias Utilizadas**
- **Python 3.x**  
- **discord.py**  
- **Binance API**  
- **Matplotlib**  
- **Requests**

---

## ⚙️ **Como Executar**

### 🔹 Pré-requisitos
- **Python 3.x** instalado.  
- Dependências do projeto instaladas:
  ```bash
  pip install -r requirements.txt
  ```
  C
  onfigurar as chaves de API da Binance e o token do Discord no código.
### 🔹 Executando o Bot
Adicione o bot ao seu servidor do Discord.

Inicie o script:
 ```bash
  python bot.py
  ```
# 🌟 Demonstração de Comandos
.moeda <nome da moeda>
Exibe informações de mercado para a moeda escolhida.
Exemplo: .moeda btc

.grafico <nome da moeda>
Gera um gráfico de preços históricos.
Exemplo: .grafico eth

.convert <quantidade> <moeda de origem> <moeda de destino>
Converte valores entre moedas.
Exemplo: .convert 100 usdt btc

.limpar <quantidade>
Limpa até 100 mensagens do chat atual.
Exemplo: .limpar 50

# 📜 Licença
Este projeto é de código aberto e pode ser utilizado para fins educacionais ou profissionais.

# ✨ Contribuições
Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.




****
