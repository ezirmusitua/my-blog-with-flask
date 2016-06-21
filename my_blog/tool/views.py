# coding=utf-8

from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required
from . import tool
from .. import db
from forms import ToolForm

@tool.route('/add', methods=['GET', 'POST'])
@login_required
def add_tool():
    pass
    """
    # TODO: after rewrite PersonalTool rewrite this
    tool_form = ToolForm()
    if tool_form.validate_on_submit():
        print tool_form.name.data
        tool_name = tool_form.name.data
        tool_desc = tool_form.desc.data
        tool_addr = tool_form.address.data
        new_tool  = PersonalTool(
            name=tool_name,
            desc=tool_desc,
            address=tool_addr
        )
        db.session.add(new_tool)
        db.session.commit()
        flash("Tool add successful")
        return redirect(url_for('main.index'))
    return render_template('tool/add_tool.html', tool_form=tool_form)
    """