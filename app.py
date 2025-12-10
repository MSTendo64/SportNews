from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Модели данных
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    news = db.relationship('News', backref='category_ref', lazy=True)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300), nullable=False)
    image_url = db.Column(db.String(200))
    date_published = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='news_ref')

# Создаем фиктивные данные для демонстрации
def create_sample_data():
    # Очищаем существующие данные
    db.drop_all()
    db.create_all()
    
    # Создаем категории
    categories = [
        Category(name='Футбол', slug='football'),
        Category(name='Хоккей', slug='hockey'),
        Category(name='Баскетбол', slug='basketball'),
        Category(name='Теннис', slug='tennis'),
        Category(name='Формула-1', slug='formula1'),
        Category(name='Бокс', slug='boxing'),
    ]
    
    for cat in categories:
        db.session.add(cat)
    
    db.session.commit()
    
    # Создаем новости
    news_list = [
        News(
            title='Сборная России одержала победу в товарищеском матче',
            content='''Российская сборная по футболу провела товарищеский матч против команды Сербии. 
            Игра завершилась со счетом 2:1 в пользу россиян. Оба гола были забиты во втором тайме. 
            Главный тренер отметил хорошую физическую подготовку команды и выразил удовлетворение результатом. 
            Следующий матч сборная проведет через две недели.''',
            short_description='Российские футболисты побеждают Сербию в товарищеском матче со счетом 2:1',
            image_url='https://images.unsplash.com/photo-1575361204480-aadea25e6e68?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            is_featured=True,
            category_id=1,
            date_published=datetime(2024, 1, 15, 10, 30),
            views=1245
        ),
        News(
            title='Новый рекорд в НХЛ: игрок сделал 5 голевых передач за матч',
            content='''В матче регулярного чемпионата НХЛ между "Торонто Мейпл Лифс" и "Эдмонтон Ойлерз" 
            был установлен новый рекорд сезона. Нападающий Коннор Макдэвид сделал 5 результативных передач, 
            что стало лучшим показателем в текущем сезоне. Его команда одержала уверенную победу со счетом 6:2.''',
            short_description='Коннор Макдэвид устанавливает рекорд сезона по количеству голевых передач',
            image_url='https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            is_featured=True,
            category_id=2,
            date_published=datetime(2024, 1, 14, 15, 45),
            views=987
        ),
        News(
            title='NBA: "Голден Стэйт" выигрывает серию из 10 матчей подряд',
            content='''Команда "Голден Стэйт Уорриорз" продолжает демонстрировать впечатляющую игру, 
            одержав десятую победу подряд в регулярном чемпионате NBA. Особенно отличился Стивен Карри, 
            набравший 42 очка в последнем матче против "Лос-Анджелес Лейкерс".''',
            short_description='"Голден Стэйт" устанавливает лучшую серию побед в сезоне NBA',
            image_url='https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            category_id=3,
            date_published=datetime(2024, 1, 13, 12, 20),
            views=765
        ),
        News(
            title='Новак Джокович выигрывает Открытый чемпионат Австралии',
            content='''Сербский теннисист Новак Джокович в очередной раз доказал свое превосходство, 
            выиграв Открытый чемпионат Австралии по теннису. В финальном матче он в четырех сетах обыграл 
            греческого теннисиста Стефаноса Циципаса. Это уже 22-й титул Большого шлема в карьере Джоковича.''',
            short_description='Джокович завоевывает 22-й титул Большого шлема в карьере',
            image_url='https://images.unsplash.com/photo-1595435934247-5d33b7f92c70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            category_id=4,
            date_published=datetime(2024, 1, 12, 9, 15),
            views=1123
        ),
        News(
            title='Новый контракт Льюиса Хэмилтона с Mercedes',
            content='''Семикратный чемпион мира Формулы-1 Льюис Хэмилтон подписал новый контракт с командой 
            Mercedes. Соглашение рассчитано на два года с опцией продления еще на один сезон. 
            Хэмилтон заявил, что планирует закончить карьеру в "Мерседесе".''',
            short_description='Льюис Хэмилтон продлевает контракт с командой Mercedes',
            image_url='https://images.unsplash.com/photo-1543351611-58f69d7c7c65?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            category_id=5,
            date_published=datetime(2024, 1, 11, 14, 10),
            views=856
        ),
        News(
            title='Подготовка к чемпионату мира по боксу началась',
            content='''Сборные команды со всего мира начали активную подготовку к предстоящему чемпионату 
            мира по боксу, который пройдет в Ташкенте. Российские боксеры проводят сборы в Кисловодске, 
            где отрабатывают тактику и технику ведения боя.''',
            short_description='Началась активная подготовка к чемпионату мира по боксу',
            image_url='https://images.unsplash.com/photo-1542849732-4914ddf6d3f7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
            category_id=6,
            date_published=datetime(2024, 1, 10, 11, 30),
            views=654
        ),
    ]
    
    for news in news_list:
        db.session.add(news)
    
    db.session.commit()

# Маршруты
@app.route('/')
def index():
    featured_news = News.query.filter_by(is_featured=True).order_by(News.date_published.desc()).limit(3).all()
    latest_news = News.query.order_by(News.date_published.desc()).limit(6).all()
    categories = Category.query.all()
    
    return render_template('index.html', 
                         featured_news=featured_news,
                         latest_news=latest_news,
                         categories=categories)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    news = News.query.get_or_404(news_id)
    news.views += 1
    db.session.commit()
    
    related_news = News.query.filter(
        News.category_id == news.category_id,
        News.id != news.id
    ).order_by(News.date_published.desc()).limit(3).all()
    
    return render_template('news_detail.html', news=news, related_news=related_news)

@app.route('/category/<slug>')
def category(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    news_pagination = News.query.filter_by(category_id=category.id)\
        .order_by(News.date_published.desc())\
        .paginate(page=page, per_page=app.config['NEWS_PER_PAGE'], error_out=False)
    
    categories = Category.query.all()
    
    return render_template('category.html',
                         category=category,
                         news_pagination=news_pagination,
                         categories=categories)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        news_pagination = News.query.filter(
            News.title.contains(query) | News.content.contains(query)
        ).order_by(News.date_published.desc())\
         .paginate(page=page, per_page=app.config['NEWS_PER_PAGE'], error_out=False)
    else:
        news_pagination = News.query.order_by(News.date_published.desc())\
            .paginate(page=page, per_page=app.config['NEWS_PER_PAGE'], error_out=False)
    
    return render_template('search.html', 
                         news_pagination=news_pagination,
                         query=query)

if __name__ == '__main__':
    with app.app_context():
        # Создаем базу данных и заполняем данными
        if not os.path.exists('sport_news.db'):
            create_sample_data()
    
    app.run(debug=True, port=5001)