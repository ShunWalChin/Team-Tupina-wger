from __future__ import annotations

import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from wger.core.models import Language
from wger.exercises.models import (
    Equipment,
    Exercise,
    ExerciseCategory,
    Muscle,
    Translation,
)
from wger.manager.models import (
    Day,
    RepetitionsConfig,
    RestConfig,
    RiRConfig,
    Routine,
    SetsConfig,
    Slot,
    SlotEntry,
)
from wger.nutrition.models import Ingredient, IngredientCategory


SOURCE_AUTHOR = 'Team Tupina / FAT Tech'
SOURCE_URL = 'https://teamtupina.com.br'


EQUIPMENT = [
    'Peso corporal',
    'Halteres',
    'Barra',
    'Anilhas',
    'Kettlebell',
    'Elástico',
    'TRX',
    'Corda naval',
    'Medicine ball',
    'Caixa pliométrica',
    'Bosu',
    'Landmine',
    'Trap bar',
    'Máquina Smith',
    'Leg press 45',
    'Hack squat',
    'Cadeira extensora',
    'Mesa flexora',
    'Cadeira flexora',
    'Cadeira abdutora',
    'Cadeira adutora',
    'Polia alta',
    'Polia baixa',
    'Cross over',
    'Remada articulada',
    'Puxada articulada',
    'Supino máquina',
    'Peck deck',
    'Desenvolvimento máquina',
    'Panturrilha máquina',
    'Esteira',
    'Bicicleta ergométrica',
    'Remo ergômetro',
]


MUSCLES = [
    ('Peitoral maior', 'Peitoral'),
    ('Latíssimo do dorso', 'Costas'),
    ('Trapézio', 'Trapézio'),
    ('Deltoide anterior', 'Ombro anterior'),
    ('Deltoide lateral', 'Ombro lateral'),
    ('Deltoide posterior', 'Ombro posterior'),
    ('Bíceps braquial', 'Bíceps'),
    ('Tríceps braquial', 'Tríceps'),
    ('Reto abdominal', 'Abdômen'),
    ('Oblíquos', 'Abdômen lateral'),
    ('Glúteo máximo', 'Glúteos'),
    ('Quadríceps', 'Coxa anterior'),
    ('Isquiotibiais', 'Coxa posterior'),
    ('Adutores', 'Parte interna da coxa'),
    ('Abdutores', 'Parte lateral do quadril'),
    ('Gastrocnêmio', 'Panturrilha'),
    ('Sóleo', 'Panturrilha profunda'),
]


CATEGORIES = [
    'Peito',
    'Costas',
    'Pernas',
    'Glúteos',
    'Ombros',
    'Braços',
    'Core',
    'Condicionamento',
    'Mobilidade',
]


EXERCISES = [
    {
        'name': 'Agachamento livre',
        'category': 'Pernas',
        'equipment': ['Barra', 'Anilhas'],
        'muscles': ['Quadríceps', 'Glúteo máximo'],
        'secondary': ['Reto abdominal', 'Isquiotibiais'],
        'description': 'Com a barra estabilizada, flexione quadril e joelhos mantendo tronco firme, pés inteiros no chão e joelhos alinhados. Suba empurrando o chão, sem perder controle lombar.',
    },
    {
        'name': 'Agachamento goblet',
        'category': 'Pernas',
        'equipment': ['Halteres', 'Kettlebell'],
        'muscles': ['Quadríceps', 'Glúteo máximo'],
        'secondary': ['Reto abdominal'],
        'description': 'Segure a carga próxima ao peito, desça com controle e mantenha cotovelos apontando para baixo. É uma variação excelente para aprender padrão de agachamento com estabilidade.',
    },
    {
        'name': 'Leg press 45',
        'category': 'Pernas',
        'equipment': ['Leg press 45'],
        'muscles': ['Quadríceps', 'Glúteo máximo'],
        'secondary': ['Isquiotibiais'],
        'description': 'Apoie os pés na plataforma, destrave a máquina e desça até manter amplitude segura. Empurre sem bloquear os joelhos e mantenha o quadril apoiado durante todo o movimento.',
    },
    {
        'name': 'Hack squat',
        'category': 'Pernas',
        'equipment': ['Hack squat'],
        'muscles': ['Quadríceps', 'Glúteo máximo'],
        'secondary': ['Reto abdominal'],
        'description': 'Com costas apoiadas e pés firmes na plataforma, desça controlando a linha dos joelhos. Suba empurrando a plataforma, priorizando amplitude consistente e ritmo estável.',
    },
    {
        'name': 'Cadeira extensora',
        'category': 'Pernas',
        'equipment': ['Cadeira extensora'],
        'muscles': ['Quadríceps'],
        'secondary': [],
        'description': 'Ajuste o encosto e o rolo na altura correta. Estenda os joelhos até contrair o quadríceps, segure brevemente no topo e retorne com controle total da carga.',
    },
    {
        'name': 'Mesa flexora',
        'category': 'Pernas',
        'equipment': ['Mesa flexora'],
        'muscles': ['Isquiotibiais'],
        'secondary': ['Gastrocnêmio'],
        'description': 'Deitado na máquina, flexione os joelhos levando o rolo em direção aos glúteos. Controle a volta e evite tirar o quadril do apoio durante a repetição.',
    },
    {
        'name': 'Elevação pélvica',
        'category': 'Glúteos',
        'equipment': ['Barra', 'Anilhas'],
        'muscles': ['Glúteo máximo'],
        'secondary': ['Isquiotibiais', 'Reto abdominal'],
        'description': 'Apoie as costas no banco, posicione a carga sobre o quadril e eleve até alinhar tronco e coxas. Contraia glúteos no topo sem hiperestender a lombar.',
    },
    {
        'name': 'Abdução de quadril na máquina',
        'category': 'Glúteos',
        'equipment': ['Cadeira abdutora'],
        'muscles': ['Abdutores', 'Glúteo máximo'],
        'secondary': [],
        'description': 'Sente-se com coluna apoiada e abra as pernas contra a resistência. Controle a volta e mantenha tensão contínua na lateral do quadril durante a série.',
    },
    {
        'name': 'Stiff com halteres',
        'category': 'Pernas',
        'equipment': ['Halteres'],
        'muscles': ['Isquiotibiais', 'Glúteo máximo'],
        'secondary': ['Reto abdominal'],
        'description': 'Segure os halteres à frente das pernas, projete o quadril para trás e mantenha a coluna neutra. Retorne contraindo glúteos e posteriores, sem transformar em agachamento.',
    },
    {
        'name': 'Panturrilha em pé',
        'category': 'Pernas',
        'equipment': ['Panturrilha máquina'],
        'muscles': ['Gastrocnêmio', 'Sóleo'],
        'secondary': [],
        'description': 'Com pés firmes no apoio, eleve os calcanhares até a contração máxima. Desça com controle até sentir alongamento, evitando saltos ou balanço corporal.',
    },
    {
        'name': 'Supino reto com barra',
        'category': 'Peito',
        'equipment': ['Barra', 'Anilhas'],
        'muscles': ['Peitoral maior'],
        'secondary': ['Tríceps braquial', 'Deltoide anterior'],
        'description': 'Deite no banco, mantenha escápulas firmes e desça a barra com controle até a linha do peito. Empurre preservando estabilidade e trajetória consistente.',
    },
    {
        'name': 'Supino inclinado com halteres',
        'category': 'Peito',
        'equipment': ['Halteres'],
        'muscles': ['Peitoral maior'],
        'secondary': ['Deltoide anterior', 'Tríceps braquial'],
        'description': 'No banco inclinado, desça os halteres ao lado do peito e suba aproximando as mãos sem bater as cargas. Mantenha punhos neutros e ritmo controlado.',
    },
    {
        'name': 'Crucifixo no peck deck',
        'category': 'Peito',
        'equipment': ['Peck deck'],
        'muscles': ['Peitoral maior'],
        'secondary': ['Deltoide anterior'],
        'description': 'Ajuste o banco para alinhar braços ao peitoral. Feche os braços contraindo o peito e retorne lentamente, sem relaxar completamente no final da fase excêntrica.',
    },
    {
        'name': 'Flexão de braços',
        'category': 'Peito',
        'equipment': ['Peso corporal'],
        'muscles': ['Peitoral maior'],
        'secondary': ['Tríceps braquial', 'Reto abdominal'],
        'description': 'Com mãos no chão e corpo alinhado, flexione os cotovelos até aproximar o peito do solo. Empurre mantendo abdômen ativo e escápulas controladas.',
    },
    {
        'name': 'Puxada alta frente',
        'category': 'Costas',
        'equipment': ['Polia alta'],
        'muscles': ['Latíssimo do dorso'],
        'secondary': ['Bíceps braquial', 'Trapézio'],
        'description': 'Segure a barra acima da cabeça, puxe em direção à parte alta do peito e conduza cotovelos para baixo. Volte controlando a subida sem perder postura.',
    },
    {
        'name': 'Remada baixa',
        'category': 'Costas',
        'equipment': ['Polia baixa'],
        'muscles': ['Latíssimo do dorso', 'Trapézio'],
        'secondary': ['Bíceps braquial', 'Deltoide posterior'],
        'description': 'Sente-se com tronco firme, puxe o pegador em direção ao abdômen e una as escápulas. Retorne com controle, mantendo ombros longe das orelhas.',
    },
    {
        'name': 'Remada curvada',
        'category': 'Costas',
        'equipment': ['Barra', 'Anilhas'],
        'muscles': ['Latíssimo do dorso', 'Trapézio'],
        'secondary': ['Bíceps braquial', 'Reto abdominal'],
        'description': 'Incline o tronco com coluna neutra, puxe a barra até a região abdominal e controle a descida. Evite usar impulso excessivo ou arredondar as costas.',
    },
    {
        'name': 'Puxada articulada',
        'category': 'Costas',
        'equipment': ['Puxada articulada'],
        'muscles': ['Latíssimo do dorso'],
        'secondary': ['Bíceps braquial'],
        'description': 'Ajuste assento e apoio, puxe as alças até aproximar cotovelos do tronco e controle a fase de retorno. Use amplitude completa sem perder encaixe escapular.',
    },
    {
        'name': 'Desenvolvimento com halteres',
        'category': 'Ombros',
        'equipment': ['Halteres'],
        'muscles': ['Deltoide anterior', 'Deltoide lateral'],
        'secondary': ['Tríceps braquial'],
        'description': 'Sentado ou em pé, empurre os halteres acima da cabeça mantendo tronco firme. Desça até a linha segura dos ombros e evite compensar com a lombar.',
    },
    {
        'name': 'Elevação lateral',
        'category': 'Ombros',
        'equipment': ['Halteres'],
        'muscles': ['Deltoide lateral'],
        'secondary': ['Trapézio'],
        'description': 'Com halteres ao lado do corpo, eleve os braços até a linha dos ombros. Controle a descida e mantenha cotovelos levemente flexionados sem balançar o tronco.',
    },
    {
        'name': 'Face pull',
        'category': 'Ombros',
        'equipment': ['Polia alta', 'Corda naval'],
        'muscles': ['Deltoide posterior', 'Trapézio'],
        'secondary': ['Bíceps braquial'],
        'description': 'Puxe a corda em direção ao rosto abrindo os cotovelos e girando levemente os braços. Foque na parte posterior dos ombros e controle a volta.',
    },
    {
        'name': 'Rosca direta',
        'category': 'Braços',
        'equipment': ['Barra'],
        'muscles': ['Bíceps braquial'],
        'secondary': [],
        'description': 'Segure a barra com pegada confortável, flexione os cotovelos sem projetá-los para frente e retorne com controle. Evite balanço para manter tensão no bíceps.',
    },
    {
        'name': 'Tríceps corda',
        'category': 'Braços',
        'equipment': ['Polia alta'],
        'muscles': ['Tríceps braquial'],
        'secondary': [],
        'description': 'Com cotovelos próximos ao corpo, empurre a corda para baixo e abra levemente as pontas no final. Retorne controlando sem deixar os ombros subirem.',
    },
    {
        'name': 'Prancha frontal',
        'category': 'Core',
        'equipment': ['Peso corporal'],
        'muscles': ['Reto abdominal'],
        'secondary': ['Oblíquos', 'Glúteo máximo'],
        'description': 'Apoie antebraços e pés no chão, mantendo corpo alinhado e abdômen ativo. Respire de forma controlada e evite deixar o quadril cair.',
    },
    {
        'name': 'Dead bug',
        'category': 'Core',
        'equipment': ['Peso corporal'],
        'muscles': ['Reto abdominal'],
        'secondary': ['Oblíquos'],
        'description': 'Deitado de barriga para cima, mova braço e perna opostos sem perder contato lombar com o chão. Execute devagar, priorizando controle respiratório.',
    },
    {
        'name': 'Pallof press',
        'category': 'Core',
        'equipment': ['Polia baixa', 'Elástico'],
        'muscles': ['Oblíquos', 'Reto abdominal'],
        'secondary': [],
        'description': 'De lado para a resistência, estenda os braços à frente do corpo e resista à rotação. Mantenha quadril estável e respiração contínua durante a série.',
    },
    {
        'name': 'Kettlebell swing',
        'category': 'Condicionamento',
        'equipment': ['Kettlebell'],
        'muscles': ['Glúteo máximo', 'Isquiotibiais'],
        'secondary': ['Reto abdominal', 'Trapézio'],
        'description': 'Use a dobradiça de quadril para impulsionar o kettlebell até a linha do peito. A força vem do quadril, com braços relaxados e coluna neutra.',
    },
    {
        'name': 'Remo ergômetro',
        'category': 'Condicionamento',
        'equipment': ['Remo ergômetro'],
        'muscles': ['Latíssimo do dorso', 'Quadríceps'],
        'secondary': ['Bíceps braquial', 'Reto abdominal'],
        'description': 'Empurre com as pernas, finalize puxando com braços e retorne em ordem inversa. Mantenha ritmo sustentável e tronco firme durante o ciclo.',
    },
    {
        'name': 'Mobilidade de quadril 90/90',
        'category': 'Mobilidade',
        'equipment': ['Peso corporal'],
        'muscles': ['Glúteo máximo', 'Abdutores'],
        'secondary': ['Adutores'],
        'description': 'Sente-se com as pernas em posição 90/90 e alterne lados com controle. Use respiração calma e amplitude sem dor para preparar quadris.',
    },
]


INGREDIENT_CATEGORIES = [
    'Proteínas magras',
    'Carboidratos base',
    'Gorduras boas',
    'Frutas',
    'Verduras e legumes',
    'Laticínios',
]


INGREDIENTS = [
    ('Peito de frango grelhado', 'Proteínas magras', 165, 31, 0, 3.6, 0, 0.7, False, False),
    ('Patinho moído cozido', 'Proteínas magras', 219, 27, 0, 12, 0, 4.8, False, False),
    ('Ovo inteiro', 'Proteínas magras', 143, 13, 1.1, 9.5, 0, 3.1, False, True),
    ('Tilápia grelhada', 'Proteínas magras', 128, 26, 0, 2.7, 0, 0.9, False, False),
    ('Tofu firme', 'Proteínas magras', 144, 15, 3, 8, 2, 1.2, True, True),
    ('Arroz integral cozido', 'Carboidratos base', 124, 2.6, 25.8, 1, 2.7, 0.2, True, True),
    ('Batata-doce cozida', 'Carboidratos base', 86, 1.6, 20, 0.1, 3, 0, True, True),
    ('Aveia em flocos', 'Carboidratos base', 389, 16.9, 66.3, 6.9, 10.6, 1.2, True, True),
    ('Feijão carioca cozido', 'Carboidratos base', 76, 4.8, 13.6, 0.5, 8.5, 0.1, True, True),
    ('Azeite de oliva', 'Gorduras boas', 884, 0, 0, 100, 0, 14, True, True),
    ('Abacate', 'Gorduras boas', 160, 2, 8.5, 14.7, 6.7, 2.1, True, True),
    ('Banana prata', 'Frutas', 89, 1.1, 22.8, 0.3, 2.6, 0.1, True, True),
    ('Maçã com casca', 'Frutas', 52, 0.3, 13.8, 0.2, 2.4, 0, True, True),
    ('Brócolis cozido', 'Verduras e legumes', 35, 2.4, 7.2, 0.4, 3.3, 0.1, True, True),
    ('Iogurte natural integral', 'Laticínios', 61, 3.5, 4.7, 3.3, 0, 2.1, False, True),
]


ROUTINES = [
    {
        'name': 'TT Reset 7 - Base',
        'description': 'Template público Team Tupiná para reinício de 7 dias com treinos curtos, consistência e execução simples.',
        'days': [
            ('Full body A', [('Agachamento goblet', 3, 12, 45, 2), ('Flexão de braços', 3, 10, 45, 2), ('Remada baixa', 3, 12, 45, 2), ('Prancha frontal', 3, 30, 30, 2)]),
            ('Cardio tabata', [('Kettlebell swing', 4, 20, 20, 3), ('Remo ergômetro', 4, 30, 30, 3)]),
            ('Mobilidade e core', [('Mobilidade de quadril 90/90', 3, 8, 30, 3), ('Dead bug', 3, 10, 30, 2), ('Pallof press', 3, 12, 30, 2)]),
        ],
    },
    {
        'name': 'TT Força Inicial 3x',
        'description': 'Template público para desenvolver base de força com grandes padrões de movimento e progressão simples.',
        'days': [
            ('Treino A', [('Agachamento livre', 3, 8, 90, 2), ('Supino reto com barra', 3, 8, 90, 2), ('Remada curvada', 3, 10, 75, 2)]),
            ('Treino B', [('Stiff com halteres', 3, 10, 75, 2), ('Desenvolvimento com halteres', 3, 10, 75, 2), ('Puxada alta frente', 3, 10, 75, 2)]),
            ('Treino C', [('Leg press 45', 3, 12, 75, 2), ('Supino inclinado com halteres', 3, 10, 75, 2), ('Remada baixa', 3, 12, 75, 2)]),
        ],
    },
    {
        'name': 'TT Hipertrofia Upper Lower 4x',
        'description': 'Template público para hipertrofia com divisão superior/inferior, volume semanal organizado e máquinas modernas.',
        'days': [
            ('Upper 1', [('Supino reto com barra', 4, 8, 90, 1.5), ('Puxada alta frente', 4, 10, 75, 1.5), ('Elevação lateral', 3, 15, 45, 2), ('Tríceps corda', 3, 12, 45, 2)]),
            ('Lower 1', [('Hack squat', 4, 10, 90, 1.5), ('Mesa flexora', 4, 12, 60, 1.5), ('Elevação pélvica', 4, 10, 75, 1.5), ('Panturrilha em pé', 4, 12, 45, 2)]),
            ('Upper 2', [('Supino inclinado com halteres', 4, 10, 75, 1.5), ('Remada baixa', 4, 10, 75, 1.5), ('Face pull', 3, 15, 45, 2), ('Rosca direta', 3, 12, 45, 2)]),
            ('Lower 2', [('Leg press 45', 4, 12, 75, 1.5), ('Stiff com halteres', 4, 10, 75, 1.5), ('Cadeira extensora', 3, 15, 45, 2), ('Abdução de quadril na máquina', 3, 15, 45, 2)]),
        ],
    },
    {
        'name': 'TT Glúteos e Pernas',
        'description': 'Template público com foco em glúteos, quadríceps e posteriores, combinando máquinas, livres e controle de esforço.',
        'days': [
            ('Glúteos força', [('Elevação pélvica', 4, 8, 90, 1.5), ('Hack squat', 4, 10, 90, 1.5), ('Abdução de quadril na máquina', 4, 15, 45, 2)]),
            ('Posterior', [('Stiff com halteres', 4, 10, 75, 1.5), ('Mesa flexora', 4, 12, 60, 1.5), ('Panturrilha em pé', 4, 12, 45, 2)]),
            ('Quadríceps', [('Leg press 45', 4, 12, 75, 1.5), ('Cadeira extensora', 4, 15, 45, 2), ('Agachamento goblet', 3, 12, 60, 2)]),
        ],
    },
    {
        'name': 'TT Condicionamento 20min',
        'description': 'Template público de condicionamento com blocos curtos, simples e escaláveis para agenda apertada.',
        'days': [
            ('Circuito A', [('Kettlebell swing', 5, 15, 30, 3), ('Flexão de braços', 5, 8, 30, 3), ('Remo ergômetro', 5, 30, 30, 3)]),
            ('Circuito B', [('Agachamento goblet', 5, 12, 30, 3), ('Pallof press', 4, 12, 30, 2), ('Prancha frontal', 4, 30, 30, 2)]),
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed Team Tupina PT-BR equipment, muscles, exercises, nutrition and public templates.'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='teamadmin')
        parser.add_argument('--skip-routines', action='store_true')
        parser.add_argument('--skip-nutrition', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        self.language = self.get_language()
        self.user = self.get_user(options['username'])
        self.equipment = self.seed_equipment()
        self.muscles = self.seed_muscles()
        self.categories = self.seed_categories()
        self.exercises = self.seed_exercises()

        if not options['skip_nutrition']:
            self.seed_nutrition()

        if not options['skip_routines']:
            self.seed_routines()

        self.stdout.write(self.style.SUCCESS('Base Team Tupina PT-BR atualizada com sucesso.'))

    def get_language(self):
        language, _ = Language.objects.get_or_create(
            short_name='pt',
            defaults={'full_name': 'Português', 'full_name_en': 'Portuguese'},
        )
        return language

    def get_user(self, username):
        User = get_user_model()
        user = User.objects.filter(username=username).first()
        if user:
            return user

        user = User.objects.create(username=username, is_staff=True, is_superuser=True)
        user.set_unusable_password()
        user.save(update_fields=['password'])
        return user

    def seed_equipment(self):
        out = {}
        for name in EQUIPMENT:
            equipment, _ = Equipment.objects.get_or_create(name=name[:50])
            out[name] = equipment
        return out

    def seed_muscles(self):
        out = {}
        for name, alias in MUSCLES:
            muscle, _ = Muscle.objects.update_or_create(
                name=name[:50],
                defaults={'name_en': alias[:50], 'is_front': name not in {'Latíssimo do dorso', 'Trapézio', 'Isquiotibiais'}},
            )
            out[name] = muscle
        return out

    def seed_categories(self):
        out = {}
        for name in CATEGORIES:
            category, _ = ExerciseCategory.objects.get_or_create(name=name)
            out[name] = category
        return out

    def seed_exercises(self):
        out = {}
        for item in EXERCISES:
            translation = Translation.objects.filter(name=item['name'], language=self.language).first()
            if translation:
                exercise = translation.exercise
                exercise.category = self.categories[item['category']]
                exercise.license_author = SOURCE_AUTHOR
                exercise.license_author_url = SOURCE_URL
                exercise.save()
            else:
                exercise = Exercise.objects.create(
                    category=self.categories[item['category']],
                    license_author=SOURCE_AUTHOR,
                    license_author_url=SOURCE_URL,
                    license_title=item['name'],
                    license_object_url=SOURCE_URL,
                )
                translation = Translation.objects.create(
                    exercise=exercise,
                    language=self.language,
                    name=item['name'],
                    description_source=item['description'],
                    license_author=SOURCE_AUTHOR,
                    license_author_url=SOURCE_URL,
                    license_title=item['name'],
                    license_object_url=SOURCE_URL,
                )

            translation.description_source = item['description']
            translation.license_author = SOURCE_AUTHOR
            translation.license_author_url = SOURCE_URL
            translation.license_title = item['name']
            translation.license_object_url = SOURCE_URL
            translation.save()

            exercise.equipment.set([self.equipment[name] for name in item['equipment']])
            exercise.muscles.set([self.muscles[name] for name in item['muscles']])
            exercise.muscles_secondary.set([self.muscles[name] for name in item['secondary']])
            out[item['name']] = exercise
        return out

    def seed_nutrition(self):
        categories = {}
        for name in INGREDIENT_CATEGORIES:
            category, _ = IngredientCategory.objects.get_or_create(name=name)
            categories[name] = category

        for name, category_name, energy, protein, carbs, fat, fiber, saturated, vegan, vegetarian in INGREDIENTS:
            Ingredient.objects.update_or_create(
                name=name,
                language=self.language,
                defaults={
                    'category': categories[category_name],
                    'common_name': name,
                    'energy': energy,
                    'protein': Decimal(str(protein)),
                    'carbohydrates': Decimal(str(carbs)),
                    'fat': Decimal(str(fat)),
                    'fiber': Decimal(str(fiber)),
                    'fat_saturated': Decimal(str(saturated)),
                    'sodium': Decimal('0'),
                    'source_name': 'Curadoria Team Tupina',
                    'source_url': SOURCE_URL,
                    'is_vegan': vegan,
                    'is_vegetarian': vegetarian,
                    'license_author': SOURCE_AUTHOR,
                    'license_author_url': SOURCE_URL,
                    'license_title': name,
                    'license_object_url': SOURCE_URL,
                },
            )

    def seed_routines(self):
        today = datetime.date.today()
        for routine_data in ROUTINES:
            routine, _ = Routine.objects.update_or_create(
                user=self.user,
                name=routine_data['name'][:25],
                defaults={
                    'description': routine_data['description'],
                    'start': today,
                    'end': today + datetime.timedelta(days=56),
                    'is_template': True,
                    'is_public': True,
                    'fit_in_week': True,
                },
            )
            routine.days.all().delete()

            for day_order, (day_name, exercises) in enumerate(routine_data['days'], start=1):
                day = Day.objects.create(
                    routine=routine,
                    order=day_order,
                    name=day_name[:20],
                    description=day_name,
                    need_logs_to_advance=False,
                )

                for slot_order, (exercise_name, sets, reps, rest, rir) in enumerate(exercises, start=1):
                    slot = Slot.objects.create(day=day, order=slot_order)
                    entry = SlotEntry.objects.create(
                        slot=slot,
                        exercise=self.exercises[exercise_name],
                        order=slot_order,
                        comment='Execução controlada, amplitude segura e carga ajustável.',
                    )
                    SetsConfig.objects.create(slot_entry=entry, iteration=1, value=sets)
                    RepetitionsConfig.objects.create(slot_entry=entry, iteration=1, value=Decimal(str(reps)))
                    RestConfig.objects.create(slot_entry=entry, iteration=1, value=rest)
                    RiRConfig.objects.create(slot_entry=entry, iteration=1, value=Decimal(str(rir)))
