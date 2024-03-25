from flask import Flask, render_template, url_for, request
import marksix, ig, multiplication, interiorAngleSum, quiz
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    title = 'SmartKits - Redefine Cramming'
    display = 'header'
    header_banner = url_for('static', filename='img/intro.png')
    return render_template('/index/index.html', title=title, display=display, header_banner=header_banner)

@app.route('/our-story')
def our_story():
    title = 'Our Story'
    display = 'title'
    return render_template('/about/our-story/our-story.html', title=title, display=display)

@app.route('/contact-us')
def contact_us():
    title = 'Contact Us'
    display = 'title'
    return render_template('/about/contact-us/contact-us.html', title=title, display=display)

@app.route('/question-keyword-dictionary')
def question_keyword_dictionary():
    title = 'Question Keyword Dictionary'
    display = 'title'
    conn = quiz.getDBConnection()
    dictionary_rows_query = '''
        SELECT
            `subjects`.`name` AS `subject_name`,
            `modules`.`name` AS `module_name`,
            `question_keywords`.`keyword` AS `keyword`,
            `question_keywords`.`meaning` AS `meaning`
        FROM `question_keywords`
        LEFT JOIN `subjects` ON `question_keywords`.`subject_id` = `subjects`.`id`
        LEFT JOIN `modules` ON `question_keywords`.`module_id` = `modules`.`id`
        ORDER BY `question_keywords`.`keyword` ASC, `question_keywords`.`meaning` ASC
    '''

    subjects_data_query = '''
        SELECT
            `subjects`.`name` AS `subject_name`
        FROM `subjects`
        ORDER BY `subject_name` ASC
    '''

    modules_data_query = '''
        SELECT
            `modules`.`name` AS `module_name`
        FROM `modules`
        ORDER BY `module_name` ASC
    '''

    dictionary_rows_data = conn.execute(dictionary_rows_query).fetchall()
    subjects_data = conn.execute(subjects_data_query).fetchall()
    modules_data = conn.execute(modules_data_query).fetchall()
    conn.close()
    return render_template('/tools/question-keyword-dictionary/question-keyword-dictionary.html', 
                           title=title, display=display,
                           dictionary_rows_data=dictionary_rows_data, 
                           subjects_data=subjects_data,
                           modules_data=modules_data
                           )

@app.route('/random-item-picker')
def random_item_picker():
    title = 'Random Item Picker'
    display = 'title'
    return render_template('/tools/random-item-picker/random-item-picker.html', 
                           title=title, display=display)

@app.route('/random-item-picker/results', methods=['POST'])
def results_random_item_picker():
    title = "Drawn Items"
    display = 'title'
    name= "Mark Six Generator"
    maxValue = int(request.form['maxValue'])
    sampleSize = int(request.form['sampleSize'])
    listItems = list(range(1, maxValue + 1))
    markSixGenerator = marksix.markSixGenerator(name, listItems, sampleSize)
    markSixGenerator.getRandomItems()
    results = markSixGenerator.getDfQuestions()["questions"]
    return render_template('/tools/random-item-picker/results.html'
                           , title=title, display=display
                           , maxValue=maxValue, sampleSize=sampleSize, results=results)

@app.route('/ig-story-vocabulary-book')
def ig_story_vocabulary_book():
    title = 'IG Story Vocabulary Book'
    display = 'title'
    conn = quiz.getDBConnection()
    all_ig_picture_query = '''
        SELECT
            `pictures`.`filename` AS `filename`
        FROM `pictures`
        WHERE `pictures`.`type` = 'ig'
    '''
    igPictures = conn.execute(all_ig_picture_query).fetchall()
    listLength = len(igPictures)
    name = "IG Story Vocabulary Book"
    listItem = list(range(1, listLength))
    sampleSize = 1
    igPictureGenerator = ig.igPictureGenerator(name, listItem, sampleSize)
    igPictureGenerator.getRandomItems()
    quizId = igPictureGenerator.getId()
    dfQuestions = igPictureGenerator.getDfQuestions()
    selectedPictureId = dfQuestions['questions'].tolist()[0]
    resultFilename = str(igPictures[(selectedPictureId)]['filename'])
    result = 'img/ig-story-vocabulary-book/' + resultFilename
    return render_template('/tools/ig-story-vocabulary-book/vocabulary-book.html', 
                           title=title,
                           display=display, quizId=quizId,
                           result=result, selectedPictureId=selectedPictureId)

@app.route('/ig-story-vocabulary-book/analysis-results', methods=['POST'])
def analysis_results_ig_story_vocabulary_book():
    title = 'Vocabulary Analysis'
    display = 'title'
    keywords = request.form['keywordInput']
    selectedPictureId = request.form['selectedPictureId']
    quizId = request.form['quizId']
    igTagAnalyzer = ig.igTagAnalyzer(keywords, quizId)
    igTagAnalyzer.findEnglishWordProfile()
    igTagAnalyzer.findRelatedWords()
    dfTags = igTagAnalyzer.getDFTags()
    dfResponses = dfTags[['quiz_id', 'tag']]
    dfResponses = dfResponses.rename(columns={'tag':'answer'})
    dfResponses['question'] = [selectedPictureId] * len(dfTags)
    quiz.storeResults(dfResponses)
    combinedData = list(zip(dfTags['tag'], dfTags['partOfSpeech'], dfTags['meaning'], dfTags['cefr'], dfTags['relatedWords']))
    return render_template('/tools/ig-story-vocabulary-book/analysis-results.html', 
                           title=title, 
                           display=display,
                           combinedData=combinedData, selectedPictureId=selectedPictureId)

@app.route('/multiplication-quiz')
def multiplication_quiz():
    title = 'Multiplication Quiz'
    display = 'title'
    name = 'Multiplication Quiz'
    sampleSize = 5
    multiplicationQuizGenerator = multiplication.multiplicationQuizGenerator(name, sampleSize)
    quizId = multiplicationQuizGenerator.getId()
    multiplicationQuizGenerator.getRandomItems()
    multiplicationQuizGenerator.getCorrectAns()
    dfQuestions = multiplicationQuizGenerator.getDfQuestions()
    questions = dfQuestions['questions'].tolist()
    correctAns = dfQuestions['correctAns'].tolist()
    combinedData = zip(questions, correctAns)
    return render_template('/tools/quiz/multiplication/multiplication-quiz.html', 
                           title=title, 
                           display=display,
                           quizId=quizId,
                           combinedData=combinedData)

@app.route('/multiplication-quiz/results', methods=['POST'])
def results_multiplication_quiz():
    title = 'Multiplication Quiz Results'
    display = 'title'
    questions = request.form.getlist('question')
    answers = request.form.getlist('answerInput')
    correctAns = request.form.getlist('correctAns')
    quizId = request.form.get('quizId')
    dfResponses = pd.DataFrame({
        "quiz_id": [quizId] * len(questions),
        "question": questions,
        "answer": answers,
        "correct_answer": correctAns
    })
    dfResponses['correct'] = dfResponses['answer'] == dfResponses['correct_answer']
    quiz.storeResults(dfResponses)
    combinedData = zip(questions, answers, correctAns)
    return render_template('/tools/quiz/multiplication/results.html', 
                           title=title, 
                           display=display,
                           combinedData=combinedData)

@app.route('/is-polygon-by-interior-angle-sum-quiz')
def is_polygon_by_interior_angle_sum_quiz():
    title = 'Is Polygon By Interior Angle Sum Quiz'
    display = 'title'
    name = 'Is Polygon By Interior Angle Sum Quiz'
    sampleSize = 5
    interiorAngleSumQuizGenerator = interiorAngleSum.interiorAngleSumQuizGenerator(name, sampleSize)
    quizId = interiorAngleSumQuizGenerator.getId()
    interiorAngleSumQuizGenerator.getRandomItems()
    interiorAngleSumQuizGenerator.getCorrectAns()
    dfQuestions = interiorAngleSumQuizGenerator.getDfQuestions()
    questions = dfQuestions['questions'].tolist()
    numberOfSides = dfQuestions['numberOfSides'].tolist()
    angleSums = dfQuestions['angleSum'].tolist()
    correctAngleSums = dfQuestions['correctAngleSum'].tolist()
    combinedData = zip(questions, numberOfSides, angleSums, correctAngleSums)
    return render_template('/tools/quiz/is-polygon-by-interior-angle-sum/is-polygon-by-interior-angle-sum-quiz.html', 
                           title=title, display=display, quizId=quizId,
                           combinedData=combinedData)

@app.route('/is-polygon-by-interior-angle-sum-quiz/results', methods=['POST'])
def results_is_polygon_by_interior_angle_sum_quiz():
    title = 'Is Polygon By Interior Angle Sum Quiz Results'
    display = 'title'
    questions = request.form.getlist('question')
    numberOfSides = request.form.getlist('numberOfSides')
    answers = request.form.getlist('answerInput')
    angleSums = request.form.getlist('angleSum')
    angleSums = [int(num) for num in angleSums]
    correctAngleSums = request.form.getlist('correctAngleSum')
    correctAngleSums = [int(num) for num in correctAngleSums]
    answers = [False if answer == 'false' else True for answer in answers]
    correctAns = [correctAngleSum == angleSum for correctAngleSum, angleSum in zip(correctAngleSums, angleSums)]
    quizId = request.form.get('quizId')
    dfResponses = pd.DataFrame({
        "quiz_id": [quizId] * len(questions),
        "question": questions,
        "answer": answers,
        "correct_answer": correctAns
    })
    dfResponses['correct'] = dfResponses['answer'] == dfResponses['correct_answer']
    quiz.storeResults(dfResponses)
    combinedData = zip(questions, numberOfSides, answers, correctAns)
    return render_template('/tools/quiz/is-polygon-by-interior-angle-sum/results.html', 
                           title=title, display=display, combinedData=combinedData)

@app.errorhandler(404)
def page_not_found(error):
    title = 'Welcome to undiscovered page!'
    display = 'title'
    return render_template('/error/page-not-found.html', title=title, display=display), 404
