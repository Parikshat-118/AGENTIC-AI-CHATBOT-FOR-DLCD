from fastapi import APIRouter

router = APIRouter()

S3_BASE_URL = "https://electromentor-pdfs.s3.amazonaws.com"

PDF_INDEX = [
    # Boolean Algebra
    {
        "id": 1,
        "title": "Boolean Algebra and Simplification Techniques",
        "category": "boolean-algebra",
        "url": f"{S3_BASE_URL}/kb/boolean-algebra/Boolean%20Algebra%20and%20Simplification%20Techniques.pdf",
    },

    # Combinational Circuits
    {
        "id": 2,
        "title": "Arithmetic Circuits",
        "category": "combinational-circuits",
        "url": f"{S3_BASE_URL}/kb/combinational-circuits/Arithmetic%20Circuits.pdf",
    },
    {
  "id": 3,
  "title": "Data Conversion Circuits (DA and AD)",
  "category": "combinational-circuits",
  "s3_key": "kb/combinational-circuits/Data Conversion Circuits DA and AD Converters.pdf",
  "url": "https://electromentor-pdfs.s3.amazonaws.com/kb/combinational-circuits/Data%20Conversion%20Circuits%20%20DA%20and%20AD%20Converters.pdf"

    },
    {
        "id": 4,
        "title": "Digital Arithmetic",
        "category": "combinational-circuits",
        "url": f"{S3_BASE_URL}/kb/combinational-circuits/Digital%20Arithmetic.pdf",
    },
    {
        "id": 5,
        "title": "Multiplexers and Demultiplexers",
        "category": "combinational-circuits",
        "url": f"{S3_BASE_URL}/kb/combinational-circuits/Multiplexers%20and%20Demultiplexers.pdf",
    },

    # Computer Fundamentals
    {
        "id": 6,
        "title": "Computer Fundamentals",
        "category": "computer-fundamentals",
        "url": f"{S3_BASE_URL}/kb/computer-fundamentals/Computer%20Fundamentals.pdf",
    },

    # Logic Gates
    {
        "id": 7,
        "title": "Logic Families",
        "category": "logic-gates",
        "url": f"{S3_BASE_URL}/kb/logic-gates/Logic%20Families.pdf",
    },
    {
        "id": 8,
        "title": "Logic Gates and Related Devices",
        "category": "logic-gates",
        "url": f"{S3_BASE_URL}/kb/logic-gates/Logic%20Gates%20and%20related%20devices.pdf",
    },

    # Microcontrollers
    {
        "id": 9,
        "title": "Microcontrollers",
        "category": "microcontrollers",
        "url": f"{S3_BASE_URL}/kb/microcontrollers/Microcontrollers.pdf",
    },

    # Microprocessors
    {
        "id": 10,
        "title": "Microprocessors",
        "category": "microprocessors",
        "url": f"{S3_BASE_URL}/kb/microprocessors/Microprocessors.pdf",
    },

    # Number Systems
    {
        "id": 11,
        "title": "Binary Codes",
        "category": "number-systems",
        "url": f"{S3_BASE_URL}/kb/number-systems/Binary%20Codes.pdf",
    },
    {
        "id": 12,
        "title": "Number Systems",
        "category": "number-systems",
        "url": f"{S3_BASE_URL}/kb/number-systems/Number%20Systems.pdf",
    },

    # Programmable Logic
    {
        "id": 13,
        "title": "Programmable Logic Devices",
        "category": "programmable-logic",
        "url": f"{S3_BASE_URL}/kb/programmable-logic/Programmable%20Logic%20Devices.pdf",
    },

    # Sequential Circuits
    {
        "id": 14,
        "title": "Counters and Registers",
        "category": "sequential-circuits",
        "url": f"{S3_BASE_URL}/kb/sequential-circuits/Counters%20and%20Registers.pdf",
    },
    {
        "id": 15,
        "title": "Flip-Flops and Related Devices",
        "category": "sequential-circuits",
        "url": f"{S3_BASE_URL}/kb/sequential-circuits/Flip-Flops%20and%20Related%20Devices.pdf",
    },

    # Troubleshooting
    {
        "id": 16,
        "title": "Troubleshooting Digital Circuits and Techniques",
        "category": "troubleshooting",
        "url": f"{S3_BASE_URL}/kb/troubleshooting/Troubleshooting%20Digital%20Circuits%20and%20Test%20Equipment.pdf",
    },
]

@router.get("/pdfs")
def list_pdfs():
    """
    Returns metadata for all PDFs.
    PDFs are loaded directly from Amazon S3.
    """
    return PDF_INDEX
