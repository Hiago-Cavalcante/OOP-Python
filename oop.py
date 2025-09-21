

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
    def __init__(self, nome, cpf=None, endereco=None, telefone=None, email=None):
        super().__init__(nome, telefone, email)
        self.cpf = cpf
        self.endereco = endereco

    def fazer_pedido(self, numero):
        return Pedido(numero, self)


class Funcionario(Pessoa):
    def __init__(self, nome, matricula=None, cargo=None, salario=0.0):
        super().__init__(nome)
        self.matricula = matricula
        self.cargo = cargo
        self.salario = salario

    def registrar_ponto(self):
        print(f"{self.nome} registrou ponto")


class Roupa:
    def __init__(self, codigo, descricao, tamanho, cor, preco, estoque):
        self.codigo = codigo
        self.descricao = descricao
        self.tamanho = tamanho
        self.cor = cor
        self.preco = float(preco)
        self.estoque = int(estoque)

    def aplicar_desconto(self, percentual):
        self.preco = self.preco * (1 - percentual / 100)

    def atualizar_estoque(self, qtd):
        self.estoque += qtd


class ItemPedido:
    def __init__(self, roupa, quantidade):
        self.roupa = roupa
        self.quantidade = int(quantidade)
        self.valor_unitario = float(roupa.preco)

    def calcular_subtotal(self):
        return self.valor_unitario * self.quantidade


class Pagamento:
    def __init__(self, valor, forma):
        self.valor = float(valor)
        self.forma = forma 
        self.status = 'PENDENTE'

    def processar(self):
        print(f"Processando pagamento de {self.valor} por {self.forma}")
        self.status = 'CONFIRMADO'

    def estornar(self):
        if self.status == 'CONFIRMADO':
            self.status = 'ESTORNADO'
            print('Pagamento estornado')
        else:
            print('Não é possível estornar pagamento não confirmado')


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []  
        self.status = 'ABERTO'
        self.pagamento = None

    def adicionar_item(self, item):
        if item.quantidade <= 0:
            print('Quantidade inválida')
            return
        if item.roupa.estoque < item.quantidade:
            print('Estoque insuficiente')
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
            print('Item não encontrado')

    def calcular_total(self):
        total = 0.0
        for it in self.itens:
            total += it.calcular_subtotal()
        return round(total, 2)

    def pagar(self, pagamento):
        self.pagamento = pagamento
        pagamento.processar()
        if pagamento.status == 'CONFIRMADO':
            self.status = 'FINALIZADO'
