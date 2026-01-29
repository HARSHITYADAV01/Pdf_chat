"""
Generate a sample PDF for testing the PDF Chat RAG application
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def create_sample_pdf(filename="sample_document.pdf"):
    """Create a sample PDF document for testing"""
    
    # Create the PDF
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    
    # Title
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER
    title = Paragraph("Artificial Intelligence and Machine Learning:<br/>A Comprehensive Overview", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Introduction
    intro_title = Paragraph("Introduction", styles['Heading2'])
    elements.append(intro_title)
    elements.append(Spacer(1, 0.1*inch))
    
    intro_text = """
    Artificial Intelligence (AI) and Machine Learning (ML) have emerged as transformative 
    technologies in the 21st century. These technologies are revolutionizing industries, 
    from healthcare to finance, and are increasingly becoming integral to our daily lives. 
    This document provides a comprehensive overview of AI and ML, their applications, 
    and future prospects.
    """
    elements.append(Paragraph(intro_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # What is AI
    ai_title = Paragraph("What is Artificial Intelligence?", styles['Heading2'])
    elements.append(ai_title)
    elements.append(Spacer(1, 0.1*inch))
    
    ai_text = """
    Artificial Intelligence refers to the simulation of human intelligence in machines 
    that are programmed to think and learn like humans. The term may also be applied to 
    any machine that exhibits traits associated with a human mind, such as learning and 
    problem-solving. AI can be categorized into two main types: Narrow AI, which is 
    designed for specific tasks, and General AI, which possesses the ability to understand, 
    learn, and apply knowledge across a wide range of tasks.
    """
    elements.append(Paragraph(ai_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Machine Learning
    ml_title = Paragraph("Understanding Machine Learning", styles['Heading2'])
    elements.append(ml_title)
    elements.append(Spacer(1, 0.1*inch))
    
    ml_text = """
    Machine Learning is a subset of AI that focuses on the development of algorithms that 
    enable computers to learn from and make decisions based on data. Rather than being 
    explicitly programmed for every task, ML systems improve their performance through 
    experience. There are three main types of machine learning: supervised learning, 
    unsupervised learning, and reinforcement learning. Each approach has its unique 
    characteristics and applications.
    """
    elements.append(Paragraph(ml_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Applications
    app_title = Paragraph("Real-World Applications", styles['Heading2'])
    elements.append(app_title)
    elements.append(Spacer(1, 0.1*inch))
    
    app_text = """
    AI and ML have found applications across numerous domains. In healthcare, they assist 
    in disease diagnosis and drug discovery. In finance, they power fraud detection systems 
    and algorithmic trading. In transportation, they enable autonomous vehicles. In 
    customer service, they drive chatbots and recommendation systems. Natural language 
    processing, computer vision, and robotics are just a few areas where these technologies 
    are making significant impacts.
    """
    elements.append(Paragraph(app_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Challenges
    challenge_title = Paragraph("Challenges and Considerations", styles['Heading2'])
    elements.append(challenge_title)
    elements.append(Spacer(1, 0.1*inch))
    
    challenge_text = """
    Despite the tremendous potential, AI and ML face several challenges. Data privacy and 
    security concerns are paramount, especially as these systems require vast amounts of 
    data. Algorithmic bias can lead to unfair or discriminatory outcomes. The lack of 
    transparency in some AI systems, often referred to as the "black box" problem, raises 
    concerns about accountability. Additionally, the potential displacement of jobs and 
    the need for workforce retraining are significant societal considerations.
    """
    elements.append(Paragraph(challenge_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Future
    future_title = Paragraph("Future Prospects", styles['Heading2'])
    elements.append(future_title)
    elements.append(Spacer(1, 0.1*inch))
    
    future_text = """
    The future of AI and ML is both exciting and uncertain. Advances in deep learning, 
    neural networks, and quantum computing promise to unlock new capabilities. We may see 
    the emergence of more sophisticated AI systems that can reason, plan, and interact 
    more naturally with humans. However, it's crucial that development proceeds with 
    careful consideration of ethical implications, ensuring that these powerful technologies 
    benefit humanity as a whole.
    """
    elements.append(Paragraph(future_text, styles['Justify']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    conclusion_title = Paragraph("Conclusion", styles['Heading2'])
    elements.append(conclusion_title)
    elements.append(Spacer(1, 0.1*inch))
    
    conclusion_text = """
    Artificial Intelligence and Machine Learning represent a paradigm shift in how we 
    approach problem-solving and decision-making. As these technologies continue to evolve, 
    they will undoubtedly play an increasingly central role in shaping our future. It is 
    imperative that researchers, policymakers, and society at large work together to 
    harness their potential while mitigating risks and ensuring equitable access to their 
    benefits.
    """
    elements.append(Paragraph(conclusion_text, styles['Justify']))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Sample PDF created: {filename}")
    print("You can use this file to test the PDF Chat application!")

if __name__ == "__main__":
    try:
        create_sample_pdf()
    except ImportError:
        print("❌ reportlab not installed. Install it with:")
        print("pip install reportlab")
