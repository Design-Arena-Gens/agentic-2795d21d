#!/usr/bin/env python3
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
PHP_DIR = ROOT / "web" / "php"
OUTPUT_DIR = ROOT / "output"
IMAGE_DIR = OUTPUT_DIR / "images"
PDF_PATH = ROOT / "web" / "public" / "task-report.pdf"


@dataclass
class Task:
    name: str
    aim: str
    problem: List[str]
    constraints: List[str]
    procedure: List[str]
    php_file: str
    conclusion: str


TASKS = [
    Task(
        name="Task 1: Largest Number Using Nested If",
        aim="Determine the largest of three numbers using nested if statements in PHP.",
        problem=[
            "Write a PHP program that accepts three predefined numbers.",
            "Use nested if statements to identify the largest value.",
            "Display the numbers and the largest number in the output.",
        ],
        constraints=[
            "Exactly three numeric values must be evaluated.",
            "Decision making must rely on nested if statements (no ternary or built-in max).",
            "Output must clearly identify the input set and the largest value.",
        ],
        procedure=[
            "Store three numeric values in an array.",
            "Assign each value to descriptive variables for clarity.",
            "Implement nested if statements comparing the numbers to find the largest.",
            "Print both the input set and the final result.",
        ],
        php_file="task1_largest.php",
        conclusion="The program successfully determines the largest number using nested if statements.",
    ),
    Task(
        name="Task 2: Reverse String Using strrev()",
        aim="Reverse a string in PHP using the built-in strrev() function.",
        problem=[
            "Write a PHP program that defines an input string.",
            "Reverse the string using the strrev() function.",
            "Display both the original and reversed strings.",
        ],
        constraints=[
            "Must utilize the strrev() function for reversing.",
            "Input string should be hard-coded for repeatable output.",
            "Output should clearly show both original and reversed values.",
        ],
        procedure=[
            "Define the string to be reversed.",
            "Call strrev() with the string and store the result.",
            "Print the original and reversed strings in separate lines.",
        ],
        php_file="task2_reverse.php",
        conclusion="The program correctly reverses the string using PHP's strrev() function.",
    ),
]


def run_php_script(file_name: str) -> str:
    script_path = PHP_DIR / file_name
    result = subprocess.run(
        ["php", str(script_path)], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def render_terminal_image(text: str, image_path: Path) -> None:
    lines = text.splitlines() or [""]
    font = ImageFont.load_default()
    line_height = font.getbbox("Ay")[3] + 6
    max_width = max(font.getbbox(line)[2] for line in lines) + 40
    height = line_height * len(lines) + 40

    image = Image.new("RGB", (max_width, height), color="white")
    draw = ImageDraw.Draw(image)

    # draw faux terminal header
    header_height = 28
    draw.rectangle([0, 0, max_width, header_height], fill="#2d2d2d")
    draw.ellipse([12, 8, 20, 16], fill="#ff5f56")
    draw.ellipse([26, 8, 34, 16], fill="#ffbd2e")
    draw.ellipse([40, 8, 48, 16], fill="#27c93f")
    y_offset = header_height + 10

    for idx, line in enumerate(lines):
        draw.text((20, y_offset + idx * line_height), line, fill="black", font=font)

    image.save(image_path)


def build_pdf(tasks: List[Task], outputs: List[str], images: List[Path]) -> None:
    pdf = FPDF(orientation="P", unit="pt", format="A4")

    # Front page
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(
        0,
        60,
        "PHP Programming Tasks Report",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(
        0,
        30,
        "Prepared for: PHP Practice Assignment",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.cell(
        0,
        30,
        "Prepared by: Codex Automation",
        align="C",
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(40)
    pdf.set_font("Helvetica", "", 14)
    pdf.multi_cell(
        pdf.epw,
        20,
        "This document presents solutions to the assigned PHP exercises, including "
        "their objectives, constraints, detailed procedures, program listings, "
        "captured outputs, and final conclusions for each task.",
    )

    # Task pages
    for task, output_text, image_path in zip(tasks, outputs, images):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 30, task.name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Aim", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(pdf.epw, 18, task.aim)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Problem Statement", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 12)
        for bullet in task.problem:
            pdf.multi_cell(pdf.epw, 18, f"- {bullet}")

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Constraints", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 12)
        for bullet in task.constraints:
            pdf.multi_cell(pdf.epw, 18, f"- {bullet}")

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Procedure", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 12)
        for idx, step in enumerate(task.procedure, start=1):
            pdf.multi_cell(pdf.epw, 18, f"{idx}. {step}")

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Program", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Courier", "", 11)
        code_lines = (PHP_DIR / task.php_file).read_text().splitlines()
        for line in code_lines:
            pdf.multi_cell(pdf.epw, 16, line)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Output", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.image(str(image_path), w=pdf.epw)
        pdf.ln(10)
        pdf.set_font("Courier", "", 11)
        for line in output_text.splitlines():
            pdf.multi_cell(pdf.epw, 16, line)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 20, "Conclusion", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(pdf.epw, 18, task.conclusion)

    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    PDF_PATH.parent.mkdir(exist_ok=True, parents=True)
    pdf.output(str(PDF_PATH))


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    outputs = []
    images = []
    for idx, task in enumerate(TASKS, start=1):
        output_text = run_php_script(task.php_file)
        outputs.append(output_text)
        image_path = IMAGE_DIR / f"task{idx}_output.png"
        render_terminal_image(output_text, image_path)
        images.append(image_path)
    build_pdf(TASKS, outputs, images)


if __name__ == "__main__":
    main()
