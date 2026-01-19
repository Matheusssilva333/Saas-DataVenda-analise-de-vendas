# 🚀 Guia de Deploy no Render (Via Blueprint)

O erro que você está vendo (`ERROR: Could not open requirements file...`) acontece porque o Render está tentando montar o projeto como um **Site Python Simples** na raiz, em vez de usar a configuração **Docker** que criamos.

Para corrigir isso, você deve usar a funcionalidade **Blueprints** do Render, que lê o arquivo `render.yaml` e configura tudo perfeitamente (Back e Front).

## Passo a Passo

1. **Acesse o Dashboard do Render**: [https://dashboard.render.com/](https://dashboard.render.com/)
2. Clique no botão **New +** e selecione **Blueprint**.
3. Conecte o seu repositório: `Saas-DataVenda-analise-de-vendas`.
4. O Render vai detectar automaticamente o arquivo `render.yaml` e mostrar dois serviços:
   - `datavenda-backend` (Docker)
   - `datavenda-frontend` (Docker)
5. Clique em **Apply** ou **Create Blueprint**.

### ⚠️ Importante sobre Variáveis
Após criar, vá na aba **Environment** de cada serviço e adicione as chaves secretas se necessário (ex: `SHOPEE_PARTNER_ID`), pois elas estão marcadas como `sync: false` no arquivo de configuração por segurança.

---

## Solução Alternativa (Se não quiser criar novo serviço)

Se você quiser consertar o serviço atual que está falhando:

1. Vá em **Settings** do serviço no Render.
2. Em **Runtime**, mude de "Python 3" para **Docker**.
3. Em **Root Directory**, defina como `backend` (se for o serviço de backend) ou `frontend` (se for o front).
4. Salve e faça um **Manual Deploy > Clear build cache & deploy**.

*Recomendamos fortemente a opção do Blueprint para garantir que frontend e backend fiquem conectados corretamente.*
