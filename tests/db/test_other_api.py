import pytest
from sqlalchemy.orm import Session

from db_requester.models import AccountTransactionTemplate
from utils.data_generator import DataGenerator


def test_accounts_transaction_template(db_session: Session):
    """
    Проверяет, что при попытке перевести сумму больше баланса — транзакция не выполняется,
    а данные в базе не изменяются.
    """

    stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=1000)
    bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)

    db_session.add_all([stan, bob])
    db_session.commit()

    # Сохраняем исходные балансы из базы
    initial_stan_balance = stan.balance
    initial_bob_balance = bob.balance

    def transfer_money(session, from_account_user, to_account_user, amount):
        """
        Имитирует логику перевода средств на стороне сервиса.
        """
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account_user).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account_user).one()

        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")

        from_account.balance -= amount
        to_account.balance += amount
        session.commit()

    assert initial_stan_balance == 1000
    assert initial_bob_balance == 500

    transfer_amount = 5000

    with pytest.raises(ValueError, match="Недостаточно средств"):
        transfer_money(db_session, from_account_user=stan.user, to_account_user=bob.user, amount=transfer_amount)

    refreshed_stan = db_session.query(AccountTransactionTemplate).filter_by(user=stan.user).one()
    refreshed_bob = db_session.query(AccountTransactionTemplate).filter_by(user=bob.user).one()

    # Проверяем, что балансы не изменились
    assert refreshed_stan.balance == initial_stan_balance, \
        f"Баланс Стэна изменился: ожидалось {initial_stan_balance}, фактически {refreshed_stan.balance}"
    assert refreshed_bob.balance == initial_bob_balance, \
        f"Баланс Боба изменился: ожидалось {initial_bob_balance}, фактически {refreshed_bob.balance}"

    print(f"Тест успешно пройден — транзакция отклонена, балансы не изменились.")

    db_session.delete(stan)
    db_session.delete(bob)
    db_session.commit()
