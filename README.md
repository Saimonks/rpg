<h1>PY-RPG: Jogo de RPG em Console (POO)</h1>
<p>Projeto de Programação Orientada a Objetos em Python.</p>

<hr>

<h2>📚 Sobre o Projeto</h2>
<p>Este é um jogo de RPG baseado em texto, desenvolvido para demonstrar os pilares da <strong>Programação Orientada a Objetos (POO)</strong>, incluindo <strong>Herança</strong>, <strong>Polimorfismo</strong>, <strong>Encapsulamento</strong> e <strong>Persistência de Dados</strong>.</p>
<p>O foco principal está na modularidade do código e na separação de responsabilidades (Classes de Modelos, Utilitários e Lógica de Jogo).</p>

<hr>

<h2>👤 Arquétipos de Personagem (Classes)</h2>
<p>O jogador pode escolher entre quatro classes, cada uma com atributos base e uma Habilidade Especial única.</p>

<table>
    <thead>
        <tr>
            <td>Classe</td>
            <td>ATK / DEF / HP Base</td>
            <td>Habilidade Especial</td>
            <td>Custo de MP</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Guerreiro</strong></td>
            <td>15 / 8 / 120</td>
            <td>Ataque Feroz (Alto Dano Físico)</td>
            <td>10</td>
        </tr>
        <tr>
            <td><strong>Mago</strong></td>
            <td>10 / 5 / 80</td>
            <td>Bola de Fogo (Alto Dano Mágico)</td>
            <td>15</td>
        </tr>
        <tr>
            <td><strong>Arqueiro</strong></td>
            <td>18 / 6 / 90</td>
            <td>Flecha Perfurante (Dano Mínimo Elevado)</td>
            <td>8</td>
        </tr>
        <tr>
            <td><strong>Curandeiro</strong></td>
            <td>5 / 7 / 100</td>
            <td>Cura Elevada (Restaura HP Alto)</td>
            <td>20</td>
        </tr>
    </tbody>
</table>

<hr>

<h2>👹 Inimigos e Chefes (BOSSES)</h2>
<p>Os inimigos normais escalam de acordo com a dificuldade (Média/Difícil). Chefes são encontros raros e garantem drops Lendários.</p>

<table>
    <thead>
        <tr>
            <td>Cenário</td>
            <td>Inimigos Comuns (Base)</td>
            <td>CHEFE (BOSS)</td>
            <td>HP Base do Chefe</td>
            <td>Item Lendário Garantido</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Floresta Sombria</td>
            <td>Goblin, Lobo Enraivecido</td>
            <td><strong>Ancião Raiz</strong></td>
            <td>250</td>
            <td>Manto da Floresta</td>
        </tr>
        <tr>
            <td>Caverna dos Cristais</td>
            <td>Morcego Gigante, Slime Brilhante</td>
            <td><strong>Golem de Pedra</strong></td>
            <td>300</td>
            <td>Cajado da Caverna</td>
        </tr>
        <tr>
            <td>Ruínas Antigas</td>
            <td>Zumbi Despertado, Esqueleto Arcano</td>
            <td><strong>Espectro Guardião</strong></td>
            <td>200</td>
            <td>Selo das Ruínas</td>
        </tr>
    </tbody>
</table>
<p><small>Chance de Boss: 5% (Média), 15% (Difícil). Chefes garantem drops Lendários. XP Fixo: 500.</small></p>

<hr>

<h2>💎 Tabela Completa de Itens (Loot e Loja)</h2>
<p>A Loja vende apenas Consumíveis básicos. Itens Equipáveis e Raros são obtidos via Loot.</p>

<table>
    <thead>
        <tr>
            <td>Item</td>
            <td>Raridade</td>
            <td>Tipo</td>
            <td>Bônus/Efeito</td>
            <td>Valor de Compra (Loja)</td>
        </tr>
    </thead>
    <tbody>
        <tr><td>Poção de Vida Pequena</td><td>Comum</td><td>Consumível</td><td>Cura 30% HP Máx.</td><td>20</td></tr>
        <tr><td>Luvas de Couro</td><td>Comum</td><td>Equipamento</td><td>DEF +1</td><td>50</td></tr>
        <tr><td>Bandagem Simples</td><td>Comum</td><td>Consumível</td><td>Restaura 15 HP fixo.</td><td>10</td></tr>
        <tr><td>Cinto de Couro</td><td>Comum</td><td>Equipamento</td><td>HP Máx +5</td><td>40</td></tr>
        <tr><td>Machado Enferrujado</td><td>Comum</td><td>Equipamento</td><td>ATK +2</td><td>60</td></tr>
        <tr><td><strong>Poção de Mana</strong></td><td>Incomum</td><td>Consumível</td><td>Restaura 15 MP.</td><td>35</td></tr>
        <tr><td><strong>Elmo de Ferro</strong></td><td>Incomum</td><td>Equipamento</td><td>DEF +3, HP Máx +5</td><td>150</td></tr>
        <tr><td><strong>Espada Longa</strong></td><td>Incomum</td><td>Equipamento</td><td>ATK +4</td><td>180</td></tr>
        <tr><td><strong>Adaga Amaldiçoada</strong></td><td>Incomum</td><td>Equipamento</td><td>ATK +5, HP Máx -10</td><td>200</td></tr>
        <tr><td><strong>Botas Leves</strong></td><td>Incomum</td><td>Equipamento</td><td>DEF +2, MP Máx +3</td><td>100</td></tr>
        <tr><td><strong>Cajado Simples</strong></td><td>Incomum</td><td>Equipamento</td><td>ATK +3, MP Máx +5</td><td>130</td></tr>
        <tr><td><strong>Amuleto da Vitalidade</strong></td><td>Raro</td><td>Equipamento</td><td>HP Máx +20, MP Máx +5</td><td>500</td></tr>
        <tr><td><strong>Pergaminho de Dano</strong></td><td>Raro</td><td>Consumível</td><td>ATK +10 Temporário.</td><td>120</td></tr>
        <tr><td><strong>Poção de Força</strong></td><td>Raro</td><td>Consumível</td><td>ATK +15 Temporário.</td><td>150</td></tr>
        <tr><td><strong>Anel de Batalha</strong></td><td>Raro</td><td>Equipamento</td><td>ATK +3, DEF +3</td><td>450</td></tr>
        <tr><td><strong>Arco de Caça</strong></td><td>Raro</td><td>Equipamento</td><td>ATK +7, HP Máx +10</td><td>600</td></tr>
        <tr><td><strong>Coração do Dragão</strong></td><td>Lendário</td><td>Equipamento</td><td>ATK +8, DEF +5, HP +30, MP +10</td><td>1500</td></tr>
        <tr><td><strong>Armadura de Obsidiana</strong></td><td>Lendário</td><td>Equipamento</td><td>DEF +12, HP +40, ATK -5</td><td>2000</td></tr>
        <tr><td><strong>Coroa do Conhecimento</strong></td><td>Lendário</td><td>Equipamento</td><td>MP Máx +50, HP +10, DEF +2</td><td>2200</td></tr>
        <tr><td><strong>Lâmina Arcana</strong></td><td>Lendário</td><td>Equipamento</td><td>ATK +15, MP Máx +20</td><td>3000</td></tr>
        <tr><td><strong>Manto da Floresta</strong></td><td>Lendário</td><td>Equipamento</td><td>DEF +7, MP Máx +15</td><td>1600</td></tr>
        <tr><td><strong>Cajado da Caverna</strong></td><td>Lendário</td><td>Equipamento</td><td>ATK +10, MP Máx +5</td><td>1800</td></tr>
        <tr><td><strong>Selo das Ruínas</strong></td><td>Lendário</td><td>Equipamento</td><td>DEF +4, HP Máx +35</td><td>1400</td></tr>
    </tbody>
</table>
<p><small>Venda de Itens: 50% do valor de compra. Itens em vermelho possuem trade-offs (penalidades).</small></p>

<hr>

<h2>✨ Funcionalidades e Mecânicas</h2>
<div>
    <ul>
        <li><strong>Morte Permanente (Permadeath):</strong> Se o herói cair em combate, o arquivo de save é deletado.</li>
        <li><strong>Sistema de Combate por Turnos:</strong> Lógica de ataque, uso de habilidade e aplicação de dano/defesa.</li>
        <li><strong>Progressão de Nível:</strong> Ganho de XP após a vitória e aumento automático de atributos ao subir de nível.</li>
        <li><strong>Inventário e Equipamento:</strong> Slots de arma/armadura com aplicação de bônus de ATK, DEF, HP Máx e MP Máx.</li>
        <li><strong>Loja (Compra/Venda):</strong> Sistema de economia básico para comprar consumíveis e vender itens por moedas.</li>
        <li><strong>Chefes Aleatórios (Bosses):</strong> Chance baixa de encontro com garantia de drops Lendários exclusivos por cenário.</li>
        <li><strong>Persistência (Save/Load):</strong> Salvamento e carregamento de objetos complexos (Personagem, Inventário, Equipamentos) usando JSON.</li>
    </ul>
</div>

<hr>

<h2>📁 Estrutura do Projeto</h2>
<p>O projeto segue a seguinte estrutura modular:</p>
<pre>
rpg_base_1/
├── models/             // Definição das classes e modelos de dados.
│   ├── base.py         // Entidade e Atributos (Base da Herança).
│   ├── classes.py      // Subclasses: Guerreiro, Mago, Arqueiro, Curandeiro.
│   ├── inimigo.py      // Classe para inimigos e chefes.
│   ├── item.py         // Definição de Item, Inventário e tabela de Loot.
│   └── personagem.py   // Lógica específica do Jogador (XP, Equipar).
│
├── utils/              // Funções de suporte.
│   └── repositorio.py  // Lógica de Save/Load em JSON.
│
├── jogo.py             // Lógica de controle, menus, lojas e geração de encontros.
└── main.py             // Ponto de entrada do programa.
</pre>

<hr>

<h2>▶️ Como Executar</h2>
<div>
    <ol>
        <li><strong>Clone o repositório:</strong></li>
        <pre><code>git clone https://github.com/Saimonks/rpg</code></pre>
        <li><strong>Navegue até a pasta:</strong></li>
        <pre><code>cd rpg_base_1</code></pre>
        <li><strong>Execute o jogo com Python:</strong></li>
        <pre><code>python main.py</code></pre>
    </ol>
</div>
<p><small>Nota: O Python pode criar pastas temporárias `__pycache__`, que são ignoradas pelo `.gitignore`.</small></p>

<hr>

<h2>👥 Desenvolvedores</h2>
<div>
    <ul>
        <li>ABRAÃO CARNEIRO SERRA</li>
        <li>ÂNGELO GARDEL SANTOS DE ANDRADE</li>
        <li>DANILO JOSÉ NUNES PEREIRA</li>
        <li>ERNESTO DA SILVA PEREIRA NETO</li>
        <li>GABRIEL VASCONCELOS DA SILVA</li>
        <li>JOSÉ MURILO ARAÚJO BRITO</li>
        <li>LUIZ FERNANDO SILVA ESPÍRITO SANTO</li>
        <li>PEDRO MATEUS ARAÚJO MELO</li>
        <li>RYAN ÁDRIAN GOMES LEITE</li>
        <li>SAIMON RUAN ALVES MOREIRA</li>
        <li>VICTOR GABRIEL BARRETO ALVES</li>
    </ul>
</div>

<footer>
    <p><strong>Orientação:</strong> Professor Mariano</p>
</footer>
