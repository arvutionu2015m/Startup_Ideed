from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import openai
from django.conf import settings
from .forms import StartupIdeaForm
from .models import StartupIdea
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import get_object_or_404
import qrcode

@login_required
def regenerate_idea(request, idea_id):
    original = get_object_or_404(StartupIdea, id=idea_id, user=request.user)

    prompt = f"""Lähtudes järgnevast huvivaldkonnast või probleemist: "{original.description}", 
loo uus startup-idee koos:

1. Ärimudel
2. Väärtuspakkumine
3. Sihtgrupp

Palun väljasta vastus punktidena."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content

    new_idea = StartupIdea(
        user=request.user,
        description=original.description,
        image=original.image,  # Soovi korral kaasa võtta
        business_model=extract_section(content, "1."),
        value_proposition=extract_section(content, "2."),
        target_audience=extract_section(content, "3."),
    )
    new_idea.save()

    return redirect('my_ideas')


def extract_section(text, section_start):
    lines = text.splitlines()
    collecting = False
    result_lines = []
    for line in lines:
        if line.strip().startswith(section_start):
            collecting = True
            continue
        elif line.strip().startswith(tuple("123456789")) and collecting:
            break
        if collecting:
            result_lines.append(line)
    return "\n".join(result_lines).strip()



def generate_idea(request):
    if request.method == 'POST':
        form = StartupIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            prompt = f"""Lähtudes järgnevast huvivaldkonnast või probleemist: "{idea.description}", 
paku startup-idee koos:

1. Ärimudel (business model),
2. Väärtuspakkumine (value proposition),
3. Sihtgrupp (target audience)

Palun väljasta täpselt selles struktuuris:"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            content = response['choices'][0]['message']['content']

            # Split vastus kolme ossa
            idea.business_model = extract_section(content, "1.")
            idea.value_proposition = extract_section(content, "2.")
            idea.target_audience = extract_section(content, "3.")
            idea.user = request.user
            idea.save()
            return render(request, 'result.html', {'idea': idea})
    else:
        form = StartupIdeaForm()
    return render(request, 'generate.html', {'form': form})


def generate_qr(request, public_id):
    idea = get_object_or_404(StartupIdea, public_id=public_id)
    url = request.build_absolute_uri(f"/idea/{idea.public_id}/")

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


def public_idea_view(request, public_id):
    idea = get_object_or_404(StartupIdea, public_id=public_id)
    return render(request, 'public_idea.html', {'idea': idea})


@login_required
def export_ideas_pdf(request):
    ideas = StartupIdea.objects.filter(user=request.user)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)

    y = 800
    for idea in ideas:
        p.drawString(50, y, f"Kirjeldus: {idea.description[:80]}...")
        y -= 20
        p.drawString(50, y, f"Tulemus: {idea.result[:100]}...")
        y -= 40
        if y < 100:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='minu_ideed.pdf')


@login_required
def export_ideas_csv(request):
    ideas = StartupIdea.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="minu_ideed.csv"'

    writer = csv.writer(response)
    writer.writerow(['Kirjeldus', 'Tulemus', 'Loodud'])

    for idea in ideas:
        writer.writerow([idea.description, idea.result, idea.created_at.strftime("%d.%m.%Y %H:%M")])

    return response


@login_required
def my_ideas(request):
    ideas = StartupIdea.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_ideas.html', {'ideas': ideas})


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_idea(request):
    if request.method == 'POST':
        form = StartupIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            prompt = f"Paku startup-idee valdkonnas: {idea.description}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            idea.result = response['choices'][0]['message']['content']
            idea.user = request.user
            idea.save()
            return render(request, 'result.html', {'idea': idea})
    else:
        form = StartupIdeaForm()
    return render(request, 'generate.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
