# =======================================================
# SISTEMA DE CONFECÇÃO DE ROUPAS - OOP + CRUD
# =======================================================

import sqlite3
from enum import Enum
from datetime import date

# =======================================================
# ENUMS
# =======================================================

class FormaPagamento(Enum):
    DINHEIRO = "Dinheiro"
    CARTAO = "Cartão"
    PIX = "Pix"
    BOLETO = "Boleto"

class StatusPagamento(Enum):
    PENDENTE = "Pendente"
    PROCESSANDO = "Processando"
    CONFIRMADO = "Confirmado"
    ESTORNADO = "Estornado"

class StatusPedido(Enum):
    ABERTO = "Aberto"
    EM_PROCESSAMENTO = "Em processamento"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"

class StatusProducao(Enum):
    PLANEJADA = "Planejada"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDA = "Concluída"
    CANCELADA = "Cancelada"

class TipoEtapa(Enum):
    CORTE = "Corte"
    COSTURA = "Costura"
    BORDADO = "Bordado"
    ACABAMENTO = "Acabamento"
    INSPECAO = "Inspeção"

# =======================================================
# CLASSES DO DOMÍNIO
# =======================================================

class Pessoa:
    def __init__(self, nome, telefone=None, email=None):
        self.nome = nome
        self.telefone = telefone
        self.email = email
    
    def atualizar_contato(self, telefone=None, email=None):
        if telefone:
            self.telefone = telefone
        if email:
            self.email = email


class Cliente(Pessoa):
    def __init__(self, nome, cpf, endereco, telefone=None, email=None):
        super().__init__(nome, telefone, email)
        self.cpf = cpf
        self.endereco = endereco
    
    def fazer_pedido(self, numero, pedido_dao):
        pedido = Pedido(numero, None, self)
        return pedido
    
    def acompanhar_pedido(self, pedido):
        print(f"Pedido {pedido.numero} está com status: {pedido.status}")
    
    def pagar_pedido(self, pedido, pagamento):
        pedido.pagar(pagamento)


class Funcionario(Pessoa):
    def __init__(self, nome, matricula, cargo, salario, telefone=None, email=None):
        super().__init__(nome, telefone, email)
        self.matricula = matricula
        self.cargo = cargo
        self.salario = salario
    
    def registrar_ponto(self):
        print(f"{self.nome} registrou ponto em {date.today()}")
    
    def calcular_salario(self):
        return self.salario


class Roupa:
    def __init__(self, codigo, descricao, tamanho, cor, preco, estoque):
        self.codigo = codigo
        self.descricao = descricao
        self.tamanho = tamanho
        self.cor = cor
        self.preco = preco
        self.estoque = estoque
    
    def aplicar_desconto(self, percentual):
        self.preco = self.preco * (1 - percentual / 100)
        print(f"Desconto aplicado! Novo preço: R$ {self.preco:.2f}")
    
    def atualizar_estoque(self, qtd):
        self.estoque += qtd
        print(f"Estoque atualizado: {self.estoque}")


class Pedido:
    def __init__(self, numero, id=None, cliente=None, status=StatusPedido.ABERTO):
        self.id = id
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = status
        self.pagamento = None
    
    def adicionar_item(self, item):
        if item.quantidade <= 0:
            print("Quantidade inválida")
            return
        if item.roupa.estoque < item.quantidade:
            print("Estoque insuficiente")
            return
        self.itens.append(item)
        item.roupa.atualizar_estoque(-item.quantidade)
        print(f"Adicionado {item.quantidade}x {item.roupa.descricao}")
    
    def remover_item(self, item):
        if item in self.itens:
            self.itens.remove(item)
            item.roupa.atualizar_estoque(item.quantidade)
            print(f"Removido {item.quantidade}x {item.roupa.descricao}")
        else:
            print("Item não encontrado")
    
    def calcular_total(self):
        return round(sum(item.calcular_subtotal() for item in self.itens), 2)
    
    def atualizar_status(self, novo_status):
        self.status = novo_status
        print(f"Pedido {self.numero} atualizado para {novo_status.value if isinstance(novo_status, Enum) else novo_status}")
    
    def pagar(self, pagamento):
        self.pagamento = pagamento
        pagamento.processar()
        pagamento.confirmar()
        if pagamento.status == StatusPagamento.CONFIRMADO:
            self.atualizar_status(StatusPedido.FINALIZADO)


class ItemPedido:
    def __init__(self, roupa, quantidade, valor_unitario=None):
        self.roupa = roupa
        self.quantidade = int(quantidade)
        self.valor_unitario = float(valor_unitario) if valor_unitario else float(roupa.preco)
    
    def calcular_subtotal(self):
        return self.valor_unitario * self.quantidade


class Pagamento:
    def __init__(self, valor, forma, pedido=None):
        self.pedido = pedido
        self.valor = float(valor)
        self.forma = forma
        self.status = StatusPagamento.PENDENTE
    
    def processar(self):
        print(f"Processando pagamento de R$ {self.valor:.2f} por {self.forma.value if isinstance(self.forma, Enum) else self.forma}")
        self.status = StatusPagamento.PROCESSANDO
    
    def confirmar(self):
        if self.status == StatusPagamento.PROCESSANDO:
            self.status = StatusPagamento.CONFIRMADO
            print("Pagamento confirmado")
    
    def estornar(self):
        if self.status == StatusPagamento.CONFIRMADO:
            self.status = StatusPagamento.ESTORNADO
            print("Pagamento estornado")
        else:
            print("Não é possível estornar pagamento não confirmado")


class Producao:
    def __init__(self, id, data_inicio=None, data_fim=None):
        self.id = id
        self.data_inicio = data_inicio or date.today()
        self.data_fim = data_fim
        self.status = StatusProducao.PLANEJADA
    
    def iniciar_producao(self):
        self.status = StatusProducao.EM_ANDAMENTO
        self.data_inicio = date.today()
        print(f"Produção {self.id} iniciada")
    
    def finalizar_producao(self):
        self.status = StatusProducao.CONCLUIDA
        self.data_fim = date.today()
        print(f"Produção {self.id} finalizada")


class EtapaProducao:
    def __init__(self, id, tipo, descricao, ordem):
        self.id = id
        self.tipo = tipo
        self.descricao = descricao
        self.ordem = ordem


class ExecucaoEtapa:
    def __init__(self, papel, funcionario=None):
        self.papel = papel
        self.funcionario = funcionario
        self.horas_trabalhadas = 0.0
        self.observacoes = ""


# =======================================================
# CLASSES DAO (DATA ACCESS OBJECT)
# =======================================================

class DAO:
    def __init__(self, db_name="confeccao.db"):
        self.db_name = db_name
    
    def conectar(self):
        return sqlite3.connect(self.db_name)


class ClienteDAO(DAO):
    def inserir(self, cliente):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pessoa (nome, telefone, email, tipo) VALUES (?, ?, ?, 'Cliente')",
                         (cliente.nome, cliente.telefone, cliente.email))
            pessoa_id = cursor.lastrowid
            cursor.execute("INSERT INTO cliente (id, cpf, endereco) VALUES (?, ?, ?)",
                         (pessoa_id, cliente.cpf, cliente.endereco))
            conn.commit()
            print(f"✅ Cliente '{cliente.nome}' cadastrado!")
    
    def listar(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nome, c.cpf, c.endereco 
                FROM pessoa p JOIN cliente c ON p.id = c.id
            """)
            print("\n📋 CLIENTES:")
            for c in cursor.fetchall():
                print(f"ID: {c[0]} | Nome: {c[1]} | CPF: {c[2]} | Endereço: {c[3]}")
    
    def deletar(self, id_cliente):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pessoa WHERE id = ?", (id_cliente,))
            conn.commit()
            print("🗑️ Cliente removido!")


class RoupaDAO(DAO):
    def inserir(self, roupa):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO roupa (codigo, descricao, tamanho, cor, preco, estoque)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (roupa.codigo, roupa.descricao, roupa.tamanho, roupa.cor, roupa.preco, roupa.estoque))
            conn.commit()
            print(f"✅ Roupa '{roupa.descricao}' cadastrada!")
    
    def listar(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo, descricao, preco, estoque FROM roupa")
            print("\n👕 ROUPAS:")
            for r in cursor.fetchall():
                print(f"ID: {r[0]} | Código: {r[1]} | {r[2]} | R$ {r[3]:.2f} | Estoque: {r[4]}")
    
    def deletar(self, id_roupa):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM roupa WHERE id = ?", (id_roupa,))
            conn.commit()
            print("🗑️ Roupa removida!")


class FuncionarioDAO(DAO):
    def inserir(self, funcionario):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pessoa (nome, telefone, email, tipo) VALUES (?, ?, ?, 'Funcionario')",
                         (funcionario.nome, funcionario.telefone, funcionario.email))
            pessoa_id = cursor.lastrowid
            cursor.execute("INSERT INTO funcionario (id, matricula, cargo, salario) VALUES (?, ?, ?, ?)",
                         (pessoa_id, funcionario.matricula, funcionario.cargo, funcionario.salario))
            conn.commit()
            print(f"✅ Funcionário '{funcionario.nome}' cadastrado!")
    
    def listar(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nome, f.matricula, f.cargo, f.salario 
                FROM pessoa p JOIN funcionario f ON p.id = f.id
            """)
            print("\n👷 FUNCIONÁRIOS:")
            for f in cursor.fetchall():
                print(f"ID: {f[0]} | Nome: {f[1]} | Matrícula: {f[2]} | Cargo: {f[3]} | Salário: R$ {f[4]:.2f}")
    
    def deletar(self, id_funcionario):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pessoa WHERE id = ?", (id_funcionario,))
            conn.commit()
            print("🗑️ Funcionário removido!")


class PedidoDAO(DAO):
    def criar(self, numero, cliente_id):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pedido (numero, cliente_id) VALUES (?, ?)", (numero, cliente_id))
            conn.commit()
            print(f"✅ Pedido '{numero}' criado!")
    
    def listar(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ped.id, ped.numero, p.nome, ped.status 
                FROM pedido ped 
                JOIN cliente c ON ped.cliente_id = c.id 
                JOIN pessoa p ON c.id = p.id
            """)
            print("\n📦 PEDIDOS:")
            for p in cursor.fetchall():
                print(f"ID: {p[0]} | Número: {p[1]} | Cliente: {p[2]} | Status: {p[3]}")


class ItemPedidoDAO(DAO):
    def adicionar(self, pedido_id, roupa_id, quantidade):
        with self.conectar() as conn:
            cursor = conn.cursor()
            # Busca preço e estoque
            cursor.execute("SELECT preco, estoque FROM roupa WHERE id = ?", (roupa_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                print("⚠️ Roupa não encontrada!")
                return
            
            preco, estoque = resultado
            
            if estoque < quantidade:
                print(f"⚠️ Estoque insuficiente! Disponível: {estoque}")
                return
            
            # Adiciona item
            cursor.execute("""
                INSERT INTO item_pedido (pedido_id, roupa_id, quantidade, valor_unitario)
                VALUES (?, ?, ?, ?)
            """, (pedido_id, roupa_id, quantidade, preco))
            
            # Atualiza estoque
            cursor.execute("UPDATE roupa SET estoque = estoque - ? WHERE id = ?", (quantidade, roupa_id))
            conn.commit()
            print(f"✅ Item adicionado! Subtotal: R$ {preco * quantidade:.2f}")
    
    def listar_por_pedido(self, pedido_id):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.descricao, ip.quantidade, ip.valor_unitario,
                       (ip.quantidade * ip.valor_unitario) as subtotal
                FROM item_pedido ip
                JOIN roupa r ON ip.roupa_id = r.id
                WHERE ip.pedido_id = ?
            """, (pedido_id,))
            print(f"\n🛒 ITENS DO PEDIDO {pedido_id}:")
            total = 0
            for item in cursor.fetchall():
                print(f"{item[0]} | Qtd: {item[1]} | Valor: R$ {item[2]:.2f} | Subtotal: R$ {item[3]:.2f}")
                total += item[3]
            print(f"\n💰 TOTAL: R$ {total:.2f}")


class PagamentoDAO(DAO):
    def inserir(self, pedido_id, valor, forma):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pagamento (pedido_id, valor, forma, status)
                VALUES (?, ?, ?, 'Pendente')
            """, (pedido_id, valor, forma))
            conn.commit()
            print(f"✅ Pagamento registrado! Forma: {forma} | Valor: R$ {valor:.2f}")
    
    def confirmar(self, pedido_id):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE pagamento SET status = 'Confirmado' WHERE pedido_id = ?", (pedido_id,))
            cursor.execute("UPDATE pedido SET status = 'Finalizado' WHERE id = ?", (pedido_id,))
            conn.commit()
            print("✅ Pagamento confirmado e pedido finalizado!")
    
    def listar(self):
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pag.id, ped.numero, pag.valor, pag.forma, pag.status
                FROM pagamento pag
                JOIN pedido ped ON pag.pedido_id = ped.id
            """)
            print("\n💳 PAGAMENTOS:")
            for p in cursor.fetchall():
                print(f"ID: {p[0]} | Pedido: {p[1]} | Valor: R$ {p[2]:.2f} | Forma: {p[3]} | Status: {p[4]}")


# =======================================================
# MENU SIMPLIFICADO
# =======================================================

def menu():
    print("\n" + "="*50)
    print("👔 SISTEMA DE CONFECÇÃO")
    print("="*50)
    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Cadastrar Funcionário")
    print("4 - Listar Funcionários")
    print("5 - Cadastrar Roupa")
    print("6 - Listar Roupas")
    print("7 - Criar Pedido")
    print("8 - Listar Pedidos")
    print("9 - Adicionar Item ao Pedido")
    print("10 - Ver Itens do Pedido")
    print("11 - Registrar Pagamento")
    print("12 - Confirmar Pagamento")
    print("13 - Listar Pagamentos")
    print("0 - Sair")
    print("="*50)


def main():
    cliente_dao = ClienteDAO()
    funcionario_dao = FuncionarioDAO()
    roupa_dao = RoupaDAO()
    pedido_dao = PedidoDAO()
    item_dao = ItemPedidoDAO()
    pagamento_dao = PagamentoDAO()
    
    while True:
        menu()
        opcao = input("Opção: ")
        
        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")
            cliente = Cliente(nome, cpf, endereco)
            cliente_dao.inserir(cliente)
        
        elif opcao == "2":
            cliente_dao.listar()
        
        elif opcao == "3":
            nome = input("Nome: ")
            matricula = input("Matrícula: ")
            cargo = input("Cargo: ")
            salario = float(input("Salário: "))
            funcionario = Funcionario(nome, matricula, cargo, salario)
            funcionario_dao.inserir(funcionario)
        
        elif opcao == "4":
            funcionario_dao.listar()
        
        elif opcao == "5":
            codigo = input("Código: ")
            descricao = input("Descrição: ")
            tamanho = input("Tamanho: ")
            cor = input("Cor: ")
            preco = float(input("Preço: "))
            estoque = int(input("Estoque: "))
            roupa = Roupa(codigo, descricao, tamanho, cor, preco, estoque)
            roupa_dao.inserir(roupa)
        
        elif opcao == "6":
            roupa_dao.listar()
        
        elif opcao == "7":
            numero = input("Número do pedido: ")
            cliente_id = int(input("ID do cliente: "))
            pedido_dao.criar(numero, cliente_id)
        
        elif opcao == "8":
            pedido_dao.listar()
        
        elif opcao == "9":
            pedido_id = int(input("ID do pedido: "))
            roupa_id = int(input("ID da roupa: "))
            quantidade = int(input("Quantidade: "))
            item_dao.adicionar(pedido_id, roupa_id, quantidade)
        
        elif opcao == "10":
            pedido_id = int(input("ID do pedido: "))
            item_dao.listar_por_pedido(pedido_id)
        
        elif opcao == "11":
            pedido_id = int(input("ID do pedido: "))
            valor = float(input("Valor: "))
            print("Forma: 1-Dinheiro | 2-Cartão | 3-Pix | 4-Boleto")
            forma_opcao = input("Escolha: ")
            formas = {"1": "Dinheiro", "2": "Cartão", "3": "Pix", "4": "Boleto"}
            forma = formas.get(forma_opcao, "Dinheiro")
            pagamento_dao.inserir(pedido_id, valor, forma)
        
        elif opcao == "12":
            pedido_id = int(input("ID do pedido: "))
            pagamento_dao.confirmar(pedido_id)
        
        elif opcao == "13":
            pagamento_dao.listar()
        
        elif opcao == "0":
            print("👋 Encerrando...")
            break


if __name__ == "__main__":
    main()
