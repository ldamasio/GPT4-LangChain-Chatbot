# chatbot.py
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from movie_database import MovieDatabase

class MovieRecommenderChatbot:
    """Chatbot especializado em recomendação de filmes usando GPT-4 e LangChain"""
    
    def __init__(self):
        # Inicializa o modelo de linguagem
        self.llm = OpenAI(
            api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        # Inicializa o banco de dados de filmes
        self.movie_db = MovieDatabase()
        
        # Template para o prompt do chatbot
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""Você é um especialista em filmes amigável e conhecedor.
            Use o histórico da conversa para dar recomendações personalizadas.
            
            Histórico da conversa:
            {history}
            
            Humano: {input}
            Assistente:"""
        )
        
        # Configura a memória da conversa
        self.memory = ConversationBufferMemory()
        
        # Cria a cadeia de conversação
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt_template,
            verbose=True
        )
    
    def get_response(self, user_input: str) -> str:
        """Processa a entrada do usuário e retorna uma resposta apropriada"""
        try:
            # Obtém a resposta do modelo
            response = self.conversation.predict(input=user_input)
            
            # Se a mensagem menciona gêneros, adiciona recomendações específicas
            genres = self._extract_genres(user_input)
            if genres:
                movies = []
                for genre in genres:
                    genre_movies = self.movie_db.get_movies_by_genre(genre)
                    movies.extend(genre_movies[:2])  # Pega até 2 filmes por gênero
                
                if movies:
                    response += "\n\nAqui estão algumas recomendações específicas:\n"
                    for movie in movies:
                        response += f"\n- {movie['title']} ({movie['year']}) - Avaliação: {movie['rating']}"
            
            return response
        
        except Exception as e:
            return f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"
    
    def _extract_genres(self, text: str) -> List[str]:
        """Extrai gêneros de filmes mencionados no texto"""
        common_genres = ['ação', 'comédia', 'drama', 'ficção científica', 'terror', 
                        'romance', 'aventura', 'animação', 'documentário']
        return [genre for genre in common_genres if genre.lower() in text.lower()]
