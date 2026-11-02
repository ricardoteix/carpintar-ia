# Marcenaria 3D Viewer

Aplicação web interativa para inspeção 3D de projetos de marcenaria com controle de **Visão Explodida** (*exploded view*), inspeção de peças e alternância de materiais.

---

## 🚀 Como Executar

Basta abrir o arquivo `index.html` diretamente em qualquer navegador moderno (Google Chrome, Microsoft Edge, Firefox):

- **Duplo clique** no arquivo `viewer/index.html` ou
- Pelo terminal:
  ```powershell
  Start-Process viewer/index.html
  ```

---

## ✨ Funcionalidades

1. **Visão Explodida Interativa**:
   - Arraste o controle deslizante de **0% a 100%** para separar as peças nos eixos exatos de montagem.
2. **Inspeção de Peças**:
   - Clique em qualquer peça no modelo 3D para destacá-la e ver suas medidas no painel lateral (comprimento, largura, espessura e coordenadas).
3. **Alternância de Materiais**:
   - Alterne instantaneamente entre **Pinus Natural**, **MDF Branco Texturizado** e **MDF Madeirado (Freijó)**.
4. **Projetos Embutidos**:
   - Cadeira Krat (Gerrit Rietveld, 1934)
   - Armário Aéreo de 2 Portas
   - Nicho Retangular de Parede
5. **Importação Customizada**:
   - Clique em **"Carregar JSON"** para abrir qualquer projeto exportado pela ferramenta MCP `export_3d_project`.
