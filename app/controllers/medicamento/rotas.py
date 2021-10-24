from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.forms import MedicamentoForm
from app.models.models import Medicamento
from app import db
from flask_login import current_user, login_required
from datetime import date

medicine = Blueprint('medicine', __name__)


@medicine.route('/medicamemento/vencido')
@login_required
def medimento_vencido():
    page = request.args.get('page', 1, type=int)
    medicamento = db.session.query(Medicamento).filter(
        Medicamento.user_id == current_user.id, Medicamento.data_validade <= date.today()).paginate(page=page, per_page=2)

    return render_template('medicamento_vencido.html', medicamentos=medicamento, title='Medicamento vencido', legenda='Medicamento Vencido')


@medicine.route('/medicamento/new', methods=['GET', 'POST'])
@login_required
def medicamento():
    form = MedicamentoForm()
    if form.validate_on_submit():
        medicamento = Medicamento(nome=form.nome.data, data_validade=form.dataValidade.data,
                                  principio_ativo=form.principioAtivo.data, posologia=form.posologia.data, user_id=current_user.id)
        db.session.add(medicamento)
        db.session.commit()

        flash('Medicamento cadastrado com sucesso..', 'success')
        return redirect(url_for('users.account'))

    return render_template('medicamento.html', title='Medicamento', legenda='Cadastro de Medicamento', form=form)


@medicine.route('/medicamento/<int:medicamento_id>/view',  methods=['GET', 'POST'])
@login_required
def view_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)

    if medicamento.user_id != current_user.id:
        abort(403)

    form = MedicamentoForm()
    form.nome.data = medicamento.nome
    form.dataValidade.data = medicamento.data_validade
    form.principioAtivo.data = medicamento.principio_ativo
    form.posologia.data = medicamento.posologia
    return render_template('medicamentoView.html', title='Medicamento', legenda='Visualiazar Medicamento', form=form, id_medicamento=medicamento_id)


@medicine.route('/medicamento/<int:medicamento_id>/update',  methods=['GET', 'POST'])
@login_required
def update_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)

    if medicamento.user_id != current_user.id:
        abort(403)

    form = MedicamentoForm()
    if form.validate_on_submit():
        medicamento.nome = form.nome.data
        medicamento.data_validade = form.dataValidade.data
        medicamento.principio_ativo = form.principioAtivo.data
        medicamento.posologia = form.posologia.data
        db.session.commit()
        flash("Medicamento Atualizado com sucesso!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.nome.data = medicamento.nome
        form.dataValidade.data = medicamento.data_validade
        form.principioAtivo.data = medicamento.principio_ativo
        form.posologia.data = medicamento.posologia
        return render_template('medicamento.html', title='Medicamento', legenda='Update de Medicamento', form=form)


@medicine.route('/medicamento/<int:medicamento_id>/delete',  methods=['POST'])
@login_required
def delete_medicamento(medicamento_id):
    medicamento = Medicamento.query.get_or_404(medicamento_id)

    if medicamento.user_id != current_user.id:
        abort(403)
    db.session.delete(medicamento)
    db.session.commit()
    flash("Medicamento removido com sucesso!", 'success')
    return redirect(url_for('users.account'))
