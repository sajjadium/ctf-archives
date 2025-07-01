# Key generation

def lfsr(state, mask):
    #Генерация нового бита и обновление состояния LFSR
    bit = (state & 1)  # Младший бит (стандартный для right-shift LFSR)
    state = state >> 1      # Сдвиг вправо
    if bit:
        state ^= mask       # Применяем маску обратной связи
    return state, bit

# Известные параметры
initial_state = 0b1100101011110001  # 16-битное начальное состояние
mask          = 0b1011010000000001  # 16-битная маска обратной связи. Примитивный полином
