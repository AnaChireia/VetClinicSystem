#!/usr/bin/env python3
"""
Teste básico dos modelos do sistema de clínica veterinária
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.tutor import Tutor
from models.pet import Pet
from models.atendimento import Atendimento
from data.database import create_tables

def test_models():
    print("=== Teste dos Modelos ===")
    
    # Criar tabelas
    create_tables()
    print("✓ Tabelas criadas")
    
    # Teste Tutor
    try:
        tutor = Tutor("João Silva", "12345678901", "(11) 99999-9999", "joao@email.com")
        tutor.salvar()
        print("✓ Tutor salvo com sucesso")
        
        tutores = Tutor.buscar_todos()
        print(f"✓ {len(tutores)} tutor(es) encontrado(s)")
        
        # Teste validações
        try:
            tutor_invalido = Tutor("Maria", "123", "(11) 99999-9999", "email_invalido")
            tutor_invalido.salvar()
            print("✗ Erro: Deveria ter falhado na validação")
        except ValueError as e:
            print(f"✓ Validação funcionou: {e}")
            
    except Exception as e:
        print(f"✗ Erro no teste de Tutor: {e}")
    
    # Teste Pet
    try:
        if tutores:
            pet = Pet("Rex", "Cão - Labrador", tutores[0].id)
            pet.salvar()
            print("✓ Pet salvo com sucesso")
            
            pets = Pet.buscar_todos()
            print(f"✓ {len(pets)} pet(s) encontrado(s)")
            
    except Exception as e:
        print(f"✗ Erro no teste de Pet: {e}")
    
    # Teste Atendimento
    try:
        pets = Pet.buscar_todos()
        if pets:
            atendimento = Atendimento(pets[0].id, "2024-01-15 10:00:00", "Consulta de rotina")
            atendimento.salvar()
            print("✓ Atendimento salvo com sucesso")
            
            atendimentos = Atendimento.buscar_todos()
            print(f"✓ {len(atendimentos)} atendimento(s) encontrado(s)")
            
            # Teste conflito
            try:
                atendimento_conflito = Atendimento(pets[0].id, "2024-01-15 10:00:00", "Outro atendimento")
                atendimento_conflito.salvar()
                print("✗ Erro: Deveria ter detectado conflito")
            except ValueError as e:
                print(f"✓ Detecção de conflito funcionou: {e}")
                
    except Exception as e:
        print(f"✗ Erro no teste de Atendimento: {e}")
    
    print("\n=== Teste Concluído ===")

if __name__ == '__main__':
    test_models()

