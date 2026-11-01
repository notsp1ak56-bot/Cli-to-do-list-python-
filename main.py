import json
import typer
#import  rich
import  os


app = typer.Typer()
def menu_programm():
    print("""
                    1. add (добавить задачу)
                    2. list (посмотеть список задач)
                    3. remove (удалить задачу)
                    4. complete (отметить решенной задачу)
                    5. resolved (посмотреть решенные задачи)
                    6. exit (Выйти из программы)

                """)

    choosr = typer.prompt("Ведите команду")
    match choosr:
        case "1":
            add()
        case "2":
            viewing()
        case "3":
            deleted()
        case "4":
            completed_task()
        case "5":
            comlete_viweng()
        case "6":
            print("Программа завершила свою работу")
        case _ :
            print("В")
            menu_programm()



def main():
    print(""""
            Программа CLI TO-Do list Запущена 
            Список функций """)
    menu_programm()





# ====================
#функции работы с Json
#====================

def viewing():

        with open("data.json", "r", encoding="utf-8") as f:
             data = json.load(f)
        for item in data:
            print(item["id"],item["text"])
        ex = input("Нажмите на Enter что бы вернуться в меню:")
        if ex == "":
            menu_programm()
        else:
            print("Вы  походу не нажали на пробел ")


def save(data):
    with open("data.json","w",encoding="UTF-8" ) as f:
        json.dump(data ,f, ensure_ascii=False,indent=2)

def add():
    input_task = input("Введите задачу:")
    if not os.path.exists("data.json"):
        data =[]
    else:
        with open("data.json", "r",encoding="UTF-8") as f:
            data = json.load(f)
    new_id = max((item["id"] for item in data ), default= 0) + 1

    data.append({
        "id": new_id
        ,"text" : input_task,
        "status": 0
    })
    save(data)
    menu_programm()

def save_done(done):
    """Вторая save — пишет в done.json. Та же логика, другой файл."""
    with open("data_completed.json", "w", encoding="utf-8") as j:
        json.dump(done, j, ensure_ascii=False, indent=4)


def load_done():
    """Читает done.json. Нет файла / битый → []."""
    if not os.path.exists("data_completed.json"):
        return []
    try:
        with open("data_completed.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def deleted():
    if not  os.path.exists("data.json"):
        print("Список пуст нечего удалять")
        return
    with open("data.json","r",encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("В списке ничего нет ")
        return
    for item in data:
        print(item["id"], item["text"])

    raw = input("Введите ID  что бы удалить задачу:").strip()
    if raw == "":
        print("Ввод пустой ")
        return
    try:
        Deleted_id = int(raw)
    except ValueError:
        print("Надо ввести целое число ")
        return
    target_index = None
    for i , item in enumerate(data):
        if item["id"] == Deleted_id:
            target_index = i
            break
    if target_index is None:
        print(f"Запись #{Deleted_id} не найден" )

    del data[target_index]

    for item in data:
        if item["id"] > Deleted_id:
            item["id"] -= 1
    save(data)
    print(f"Удалено #{Deleted_id}.Осалось Записей: {len(data)}")
    menu_programm()


def completed_task():
    # 1. Читаем data.json
    if not os.path.exists("data.json"):
        print("Нет задач")
        return                                   # ← ВНУТРИ if
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        print("Нет задач")
        return

    # 2. Показываем id и text (status скрыт)
    for item in data:
        print(item["id"], item["text"])

    # 3. Спрашиваем id
    raw = input("Введите id задачи для отметки выполненной: ").strip()
    if raw == "":
        print("Пустой ввод — отмена")
        return
    try:
        task_id = int(raw)
    except ValueError:
        print("Введите целое число")
        return

    # 4. Ищем индекс
    target_index = None
    for i, item in enumerate(data):
        if item["id"] == task_id:
            target_index = i
            break

    if target_index is None:
        print(f"Задача #{task_id} не найдена")
        return

    # 5. Уже выполнена?
    if data[target_index].get("status", 0) == 1:
        print(f"Задача #{task_id} уже выполнена")
        return

    # 6. Помечаем и вынимаем из data
    data[target_index]["status"] = 1
    finished = data.pop(target_index)            # убирает из data и возвращает

    # 7. Читаем done.json (или [])
    if not os.path.exists("done.json"):
        done = []
    else:
        with open("done.json", "r", encoding="utf-8") as f:
            done = json.load(f)

    # 8. Дописываем и сохраняем ОБА файла
    done = load_done()
    done.append(finished)
    save_done(done)                              # сначала done — чтобы не потерять
    save(data)

    # потом data — уже без неё

    print(f"Задача #{task_id} перенесена в done.json")
    menu_programm()


def comlete_viweng():
    if not os.path.exists("data_completed.json"):
        return []
    with open("data_completed.json","r",encoding="utf-8") as j:
        data = json.load(j)
    for item in data:
        print(item["id"], item["text"])

    ex = input("Нажмите на Enter что бы вернуться в меню:")
    if ex == "":
        menu_programm()
    else:
        print("Вы  походу не нажали на пробел ")



if __name__ == "__main__":
    main()





