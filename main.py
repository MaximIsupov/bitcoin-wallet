import sqlite3
import tkinter as tk
from tkinter import ttk
import requests
from bit import PrivateKeyTestnet


conn = sqlite3.connect('main.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS contacts(address TEXT PRIMARY KEY, fname TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS current_user(wif TEXT PRIMARY KEY, address TEXT)")
conn.commit()
wifDB = cur.execute("SELECT * FROM current_user;")
userInfo = wifDB.fetchone()
contactsDB = cur.execute("SELECT * FROM contacts;")
contactsInfo = contactsDB.fetchall()
print(contactsInfo)

print(userInfo)
root = tk.Tk()
root.title("Bitcoin-кошелёк")
if (userInfo):
    addressValue = tk.Label(root, text=userInfo[1], font=("Roboto", 14))
    wifValue = tk.Label(root, text=userInfo[0], font=("Roboto", 14))
else:
    addressValue = tk.Label(root, text="Введите свой WIF ключ:", font=("Roboto", 14))
    wifValue = tk.Label(root, text="undefined", font=("Roboto", 14))
root.geometry("665x360")
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
results = tk.Text(tab1, wrap='word', height=8, font=("Roboto", 11))
results2 = tk.Text(tab2, wrap='word', height=14, font=("Roboto", 11))
results3 = tk.Text(tab3, wrap='word', height=7, font=("Roboto", 11))
results4 = tk.Text(tab4, wrap='word', height=7, font=("Roboto", 11))
tab_control.add(tab1, text="Ваш кошелёк")
tab_control.add(tab2, text="Баланс кошелька")
tab_control.add(tab3, text="Транзакции")
tab_control.add(tab4, text="Контакты")
if (userInfo):
    results.insert(1.0, "Ваш публичный адрес = " + userInfo[1])
else:
    results.insert(1.0, "Введите свой wif ключ для добавления кошелька")
results2.insert(1.0, "Вы ещё не запрашивали баланс кошелька")
results3.insert(1.0, "Новых транзакций пока не совершалось")
results4.insert(1.0, "")
resultsCurrentRow = 1.0
for contact in contactsInfo:
    print(contact)
    results4.insert(resultsCurrentRow, contact[0] + " " + contact[1] + '\n')
address = tk.Label(tab1, text="Адрес вашего кошелька: " + addressValue['text'], font=("Roboto", 14))
changeAddresLabel = tk.Label(tab1, text="Или импортируйте свой ключ: ", font=("Roboto", 12))
changeAddresEntry = tk.Entry(tab1, width=50)
changeAddresButton = tk.Button(tab1, text="Изменить адрес кошелька", font=("Roboto", 12), width=30, bg='#ace8cb')
sendLabel = tk.Label(tab3, text="Создание новой транзакции", font=("Roboto", 14))
sendAddressLabel = tk.Label(tab3, text="Введите адрес получателя", font=("Roboto", 12))
sendAddressEntry = tk.Entry(tab3, width=50)
sendValueLabel = tk.Label(tab3, text="Введите количество монет", font=("Roboto", 12))
sendValueEntry = tk.Entry(tab3, width=50)
sendButton = tk.Button(tab3, text="Отправить сумму", font=("Roboto", 12), width=30, bg='#ace8cb')
contactsLabel = tk.Label(tab4, text="Контакты", font=("Roboto", 14))
deleteContactsButton = tk.Button(tab4, text="Очистить контакты", font=("Roboto", 12), width=30, bg='#ace8cb')
addContactLabel = tk.Label(tab4, text="Введите адрес контакта", font=("Roboto", 12))
addContactEntry = tk.Entry(tab4, width=50)
addContactNameLabel = tk.Label(tab4, text="Введите имя контакта", font=("Roboto", 12))
addContactNameEntry = tk.Entry(tab4, width=50)
addContactButton = tk.Button(tab4, text="Добавить", font=("Roboto", 12), width=30, bg='#ace8cb')
btn = tk.Button(tab1,
                text="Создать новый кошелёк",
                font=("Roboto", 12),
                width=20,
                bg="#ace8cb",
                fg="black")
btn2 = tk.Button(tab2,
                text="Получить информацию о балансе и транзакциях",
                font=("Roboto", 12),
                width=50,
                height=1,
                bg="#ace8cb",
                fg="black")


def sendTransaction(event):
    if (sendAddressEntry.get() and sendValueEntry.get()):
        source_k = PrivateKeyTestnet(wifValue['text'])
        results3.delete(1.0, tk.END)
        results3.insert(1.0, f'Отправка от  {source_k.address} на адрес {sendAddressEntry.get()}')
        print(f'Отправка от  {source_k.address} to {sendAddressEntry.get()}')
        r = source_k.send([
            (sendAddressEntry.get(), float(sendValueEntry.get()), 'btc')
        ])
        results3.insert(2.0, f'\nДля просмотра транзакции в Blockcypher Explore перейдите по ссылке: '
                             f'https://live.blockcypher.com/btc-testnet/tx/{r}')
        print(r)  # ID транзакции
        sendAddressEntry.delete(0, 'end')
        sendValueEntry.delete(0, 'end')


def createWallet(event):
    results.delete(1.0, tk.END)
    my_key = PrivateKeyTestnet()
    results.insert(1.0, "Ваша версия ключа: " + my_key.version + '\n')
    print("Ваша версия ключа: " + my_key.version)
    addressValue['text'] = my_key.address
    address['text'] = "Адрес вашего кошелька: " + my_key.address
    results.insert(2.0, "Ваш wif-ключ: " + my_key.to_wif() + '\n')
    print("Ваш wif-ключ: " + my_key.to_wif())
    wifValue['text'] = my_key.to_wif()
    results.insert(3.0, "Ваш адрес: " + my_key.address + '\n')
    print("Ваш адрес: " + my_key.address)
    results.insert(4.0, "Обязательно сохраните полученный ключ")
    cur.execute("DELETE FROM current_user")
    cur.execute("INSERT INTO current_user(wif, address) VALUES (?, ?)", (my_key.to_wif(), my_key.address))
    conn.commit()


def checkBalance(event):
    wallet = addressValue['text']
    url = f'https://api.blockcypher.com/v1/btc/test3/addrs/{wallet}/full?limit = 50'
    x = requests.get(url)
    wallet = x.json()
    results2.delete(1.0, tk.END)
    results2.insert(1.0, 'Информация по кошельку ' + str(wallet['address']) + ': \n')
    results2.insert(2.0, 'Всего получено: ' + str(wallet['total_received']) + '\n')
    results2.insert(3.0, 'Всего отправлено: ' + str(wallet['total_sent']) + '\n')
    results2.insert(4.0, 'Баланс на текущий момент: ' + str(wallet['balance']) + '\n')
    results2.insert(5.0, 'Неподтверждённый баланс: ' + str(wallet['unconfirmed_balance']) + '\n')
    results2.insert(6.0, 'Итоговый баланс(Подтверждённый и нет): ' + str(wallet['final_balance']) + '\n')
    results2.insert(7.0, 'Количество транзакций с кошельком: ' + str(wallet['n_tx']) + '\n')
    results2.insert(8.0, 'Количество неподтверждённых транзакций: ' + str(wallet['unconfirmed_n_tx']) + '\n')
    results2.insert(9.0, 'Итоговое количество транзакций: ' + str(wallet['final_n_tx']) + '\n')




def changeAddress(event):
    if(changeAddresEntry.get() != ''):
        myKey = PrivateKeyTestnet(changeAddresEntry.get())
        cur.execute("DELETE FROM current_user")
        cur.execute("INSERT INTO current_user(wif, address) VALUES (?, ?)", (myKey.to_wif(), myKey.address))
        addressValue['text'] = myKey.address
        wifValue['text'] = myKey.to_wif()
        conn.commit()
        address['text'] = "Адрес вашего кошелька: " + myKey.address


def addContact(event):
    if (addContactNameEntry.get() != '' and addContactEntry != ''):
        cur.execute("INSERT OR IGNORE INTO contacts(address, fname) VALUES (?, ?)", (addContactEntry.get(), addContactNameEntry.get()))
        conn.commit()
        results4.insert(1.0, addContactEntry.get() + " " + addContactNameEntry.get() + "\n")
        addContactNameEntry.delete(0, 'end')
        addContactEntry.delete(0, 'end')


def deleteContacts(event):
    cur.execute("DELETE FROM contacts")
    results4.delete(1.0, tk.END)
    conn.commit()

btn.bind("<Button-1>", createWallet)
btn2.bind("<Button-1>", checkBalance)
changeAddresButton.bind("<Button-1>", changeAddress)
sendButton.bind("<Button-1>", sendTransaction)
addContactButton.bind("<Button-1>", addContact)
deleteContactsButton.bind("<Button-1>", deleteContacts)

tab_control.pack(expand=1, fill='both')
address.grid(row=0, column=0, columnspan=3, pady=10, ipadx=10)
changeAddresLabel.grid(row=1, column=0, pady=10)
changeAddresEntry.grid(row=1, column=1, pady=10)
changeAddresButton.grid(row=2, column=1, pady=10)
btn.grid(row=2, column=0, pady=20)
btn2.grid(row=0, column=0, columnspan=2, pady=20)
sendLabel.grid(row=0, column=1, pady=10)
sendAddressLabel.grid(row=1, column=0, pady=10)
sendAddressEntry.grid(row=1, column=1, pady=10, padx=10)
sendValueLabel.grid(row=2, column=0, pady=10)
sendValueEntry.grid(row=2, column=1, pady=10, padx=10)
sendButton.grid(row=3,columnspan=2, pady=10)
results.grid(row=3, column=0, columnspan=2, padx=10, ipady=9)
results2.grid(row=1, column=0, columnspan=2, padx=10, ipady=5)
results3.grid(row=4, column=0, columnspan=2, padx=10, ipady=5)
contactsLabel.grid(row=0, column=1, pady=10)
results4.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
addContactLabel.grid(row=1, column=0, pady=10)
addContactEntry.grid(row=1, column=1)
addContactButton.grid(row=3, pady=10, column=0)
addContactNameLabel.grid(row=2, column=0, pady=10)
addContactNameEntry.grid(row=2, column=1, pady=10)
deleteContactsButton.grid(row=3, column=1, pady=10)
root.mainloop()