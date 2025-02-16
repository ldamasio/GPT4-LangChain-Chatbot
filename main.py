# main.py

from chatbot import MovieRecommenderChatbot
def main():
    """Função principal para executar o chatbot"""
    print("Bem-vindo ao Assistente de Recomendação de Filmes!")
    print("Digite 'sair' para encerrar a conversa.")
    
    # Inicializa o chatbot
    chatbot = MovieRecommenderChatbot()
    
    while True:
        # Obtém input do usuário
        user_input = input("\nVocê: ").strip()
        
        # Verifica se o usuário quer sair
        if user_input.lower() == 'sair':
            print("\nObrigado por usar o Assistente de Recomendação de Filmes! Até logo!")
            break
        
        # Obtém e exibe a resposta do chatbot
        response = chatbot.get_response(user_input)
        print(f"\nAssistente: {response}")

if __name__ == "__main__":
    main()