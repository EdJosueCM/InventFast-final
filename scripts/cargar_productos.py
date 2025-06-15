import random
from application.core.models import Producto, Marca, Categoria

def run():
    marcas = list(Marca.objects.all())
    categorias = list(Categoria.objects.all())

    if not marcas or not categorias:
        print("🚫 No hay marcas o categorías suficientes.")
        return

    nombres_productos = [
        "Leche Entera", "Yogur Natural", "Pan Integral", "Manzanas Rojas", "Naranjas Dulces",
        "Cereal Crunchy", "Jugo de Naranja", "Queso Fresco", "Huevos Orgánicos", "Aceite de Girasol",
        "Arroz Blanco", "Harina Integral", "Pollo Congelado", "Café Molido", "Galletas de Avena",
        "Atún en Lata", "Salsa de Tomate", "Azúcar Morena", "Sal yodada", "Fideos de Trigo",
        "Jabón Líquido", "Shampoo Anticaspa", "Cepillo de Dientes", "Crema Corporal", "Detergente Líquido",
        "Desinfectante Multiusos", "Papel Higiénico", "Toalla de Cocina", "Limpia Vidrios", "Suavizante",
        "Laptop UltraThin", "Audífonos Bluetooth", "Teclado Inalámbrico", "Mouse Ergonómico", "Smartphone X",
        "Cargador USB-C", "Memoria USB 32GB", "Tablet Compacta", "Monitor LED 24\"", "Impresora Multifunción",
        "Martillo Antideslizante", "Destornillador Cruz", "Taladro Eléctrico", "Llave Inglesa", "Brochas para Pintar",
        "Foco LED", "Regleta Eléctrica", "Alargador de Corriente", "Lámpara de Escritorio", "Extintor Portátil",
        "Croquetas para Perros", "Arena para Gatos", "Juguete para Mascotas", "Alimento para Peces", "Collar Reflectante",
        "Maceta de Plástico", "Fertilizante Líquido", "Tierra para Plantas", "Rastrillo de Jardín", "Regadera Manual",
        "Sillón Reclinable", "Mesa de Madera", "Cojín Decorativo", "Cortinas de Tela", "Alfombra Moderna",
        "Camiseta Básica", "Pantalón Jeans", "Zapatillas Deportivas", "Calcetines de Algodón", "Chaqueta Impermeable",
        "Licuadora de Vidrio", "Cafetera Programable", "Sartén Antiadherente", "Olla a Presión", "Batidora Manual",
        "Libro de Cocina", "Agenda 2025", "Cuaderno Universitario", "Lapiceros de Gel", "Resaltadores Pastel",
        "Colonia Refrescante", "Maquillaje Natural", "Crema Facial", "Protector Solar", "Toallas Húmedas",
        "Soda Natural", "Agua con Gas", "Energizante Max", "Té Verde", "Jugo Detox",
        "Chocolate en Tableta", "Caramelos Mixtos", "Galletas de Chocolate", "Cereal Avena Mix", "Granola Crunch",
        "Cepillo para Cabello", "Peine Plegable", "Gel Fijador", "Espuma Volumen", "Mascarilla Capilar"
    ]

    productos_creados = 0
    for nombre in nombres_productos:
        marca = random.choice(marcas)
        categoria = random.choice(categorias)

        # Validar si ya existe esa combinación de nombre + marca
        if Producto.objects.filter(nombre=nombre, marca=marca).exists():
            continue  # saltar si ya existe

        Producto.objects.create(
            nombre=nombre,
            marca=marca,
            categoria=categoria,
            descripcion=f"{nombre} de la marca {marca.nombre}, categoría {categoria.nombre}.",
            cantidad=random.randint(5, 100),
            precio=round(random.uniform(2.0, 150.0), 2)
        )
        productos_creados += 1

    print(f"✅ Se crearon {productos_creados} productos únicos.")
