"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                     🔥 REYNA MODA v2.0 🔥                                ║
║                                                                           ║
║  Punto de entrada compatible con la nueva estructura modular              ║
║                                                                           ║
║  ✅ COMANDO RECOMENDADO:                                                 ║
║  python -m uvicorn backend.app.main:app --reload                         ║
║                                                                           ║
║  📍 Servidor: http://localhost:8000                                      ║
║  📚 Docs: http://localhost:8000/docs                                     ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
