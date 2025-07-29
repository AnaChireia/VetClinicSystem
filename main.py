#!/usr/bin/env python3
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import main

if __name__ == '__main__':
    main()

