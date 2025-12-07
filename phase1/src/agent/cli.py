import sys
from src.agent.manager import TodoManager

def main():
    agent = TodoManager()
    
    # If args provided, process single command
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(agent.run(user_input))
        return

    # Interactive mode
    print(f"🤖 {agent.name} initialized.")
    print(f"Persona: {agent.persona}")
    print("Type 'help' to see what I can do, or 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            response = agent.run(user_input)
            print(f"Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
