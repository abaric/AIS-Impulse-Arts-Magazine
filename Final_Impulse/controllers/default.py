from gluon.tools import datetime
from gluon.tools import Auth
        

def user():
    return dict(form=auth())
    
def load_roles():
        session.roles=[]
        if auth.has_membership('arts_board'):
            session.user_arts_board_id=db(db.arts_board.email==auth.arts_board.email).select().first().id
            a=('arts_board','index',session.user_arts_board_id)
            session.roles.append(a)
        return locals()
                                      
def index():
    return locals()

def download():
    return response.download(request, db)

def show_image_comments():
    image_form=SQLFORM(db.image,fields=['title','file'],labels={'file':'Your Image'})
    image_form.vars.author_id=auth.user.id
    image_form.add_button('Back', URL('index'))
    if image_form.process().accepted:
        response.flash='image post submitted!'
    images=db(db.image).select(db.image.ALL, orderby=db.image.id)
    
    d={}
    for image in images:
        comments=db((db.image_comment.image_id==image.id) &\
                   (db.auth_user.id==db.image_comment.author_id)).select() 
        tuple_list=[]       
        for comment in comments:
            author=('%s %s')%(comment.auth_user.first_name,comment.auth_user.last_name)
            body=('%s')%(comment.image_comment.body)
            t=(author,body)
            tuple_list.append(t)
        d[image.id]=tuple_list
  
    form = SQLFORM(db.writing_comment)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    #images = db(db.image_comment.image_id==image.id).select()
    return locals()
    
def show_writing_comments():
    writing_form=SQLFORM(db.writing,fields=['title','body'],labels={'body':'Insert your post'})
    writing_form.vars.author_id=auth.user.id
    writing_form.add_button('Back', URL('index'))
    if writing_form.process().accepted:
        response.flash='writing post submitted!'
   
    writings=db(db.writing).select(db.writing.ALL, orderby=db.writing.id)
    d={}
    for writing in writings:
        comments=db((db.writing_comment.writing_id==writing.id) &\
                   (db.auth_user.id==db.writing_comment.author_id)).select() 
        tuple_list=[]       
        for comment in comments:
            author=('%s %s')%(comment.auth_user.first_name,comment.auth_user.last_name)
            body=('%s')%(comment.writing_comment.body)
            t=(author,body)
            tuple_list.append(t)
        d[writing.id]=tuple_list
  
    form = SQLFORM(db.writing_comment)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    return locals()

def show_video_comments():
    video_form=SQLFORM(db.video,fields=['title','url_str'],labels={'url_str':'Insert url string per above directions'})
    video_form.vars.author_id=auth.user.id
    video_form.add_button('Back', URL('index'))
    if video_form.process().accepted:
        response.flash='video post submitted!'
    
    videos=db(db.video).select(db.video.ALL, orderby=db.video.id)
    d={}
    for video in videos:
        comments=db((db.video_comment.video_id==video.id) &\
                   (db.auth_user.id==db.video_comment.author_id)).select() 
        tuple_list=[]       
        for comment in comments:
            author=('%s %s')%(comment.auth_user.first_name,comment.auth_user.last_name)
            body=('%s')%(comment.video_comment.body)
            t=(author,body)
            tuple_list.append(t)
        d[video.id]=tuple_list
    form = SQLFORM(db.video_comment)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    return locals()  

def insert_writing_comment():
    if auth.user:
        writing_comment=request.post_vars.writing_comment
        writing_id=request.args(0)
        db.writing_comment.insert(author_id=auth.user.id,
                                  writing_id=writing_id,
                                  email=None,
                                  body=writing_comment,
                                  date_of_entry=datetime.datetime.today())
        db.commit()
       
    else:
        session.flash='You must log in to post a comment.'
    redirect(URL('show_writing_comments'))
    return locals()


def insert_image_comment():
    if auth.user:
        image_comment=request.post_vars.image_comment
        image_id=request.args(0)
        db.image_comment.insert(author_id=auth.user.id,
                                  image_id=image_id,
                                  email=None,
                                  body=image_comment,
                                  date_of_entry=datetime.datetime.today())
        db.commit()
       
    else:
        session.flash='You must log in to post a comment.'
    redirect(URL('show_image_comments'))
    return locals()
    
def insert_video_comment():
    if auth.user:
        video_comment=request.post_vars.video_comment
        video_id=request.args(0)
        db.video_comment.insert(author_id=auth.user.id,
                                  video_id=video_id,
                                  email=None,
                                  body=video_comment,
                                  date_of_entry=datetime.datetime.today())
        db.commit()
       
    else:
        session.flash='You must log in to post a comment.'
    redirect(URL('show_video_comments'))
    return locals()

def all_media():
    images=db(db.image).select(db.image.ALL)
    writings=db(db.writing).select(db.image.ALL)
    videos=db(db.video).select(db.video.ALL)
    
    images_with_app=[]
    images_wo_app=[]
    videos_with_app=[]
    videos_wo_app=[]
    writings_with_app=[]
    writings_wo_app=[]
    
    for image in images:
        if image.image.approved:
            images_w_app.append(image)
        else:
            images_wo_app.append(image)
            
    for video in videos:
        if video.video.approved:
            videos_w_app.append(video)
        else:
            videos_wo_app.append(video)
    
    for writing in wristing:
        if writing.writing.approved:
            writings_w_app.append(writing)
        else:
            writings_wo_app.append(writing)
    
    return locals()


#def update_approve():
