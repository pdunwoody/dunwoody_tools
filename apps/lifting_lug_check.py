import marimo

__generated_with = "0.13.13"
app = marimo.App(app_title="Lifting Lug Evaluation")


@app.cell
def _():
    #Imports and global constants setup
    import math as m
    import pint
    import marimo as mo
    import os

    u = pint.UnitRegistry()
    return m, mo, os, u


@app.cell
def _(mo):
    mo.md(r"""## Working Load Limit""")
    return


@app.cell(hide_code=True)
def _(mo):
    WLL_input = mo.ui.number(value=30000, label="WLL (lbf): ")
    WLL_unit = mo.ui.dropdown(value="lbf", options=["lbf", "ton_force", "N", "kN", "metric_ton_force"])

    mo.hstack([WLL_input, WLL_unit], justify="start")
    return WLL_input, WLL_unit


@app.cell
def _(WLL_input, WLL_unit, u):
    # Working Load Limit
    WLL = u.Quantity(WLL_input.value, WLL_unit.value)
    WLL
    return (WLL,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Dimensions""")
    return


@app.cell(hide_code=True)
def _(mo):
    # Lug Dimensions
    length_units=["inch", "mm", "ft", "m"]
    t_input = mo.ui.number(value=1.5, label="Thickness: ")
    t_unit = mo.ui.dropdown(value="inch", options=length_units)
    w1_input = mo.ui.number(value=4.5, label="w1: ")
    w1_unit = mo.ui.dropdown(value="inch", options=length_units)
    w2_input = mo.ui.number(value=4.5, label="w2: ")
    w2_unit = mo.ui.dropdown(value="inch", options=length_units)
    h1_input = mo.ui.number(value=4.0, label="h1: ")
    h1_unit = mo.ui.dropdown(value="inch", options=length_units)
    h2_input = mo.ui.number(value=4.0, label="h2: ")
    h2_unit = mo.ui.dropdown(value="inch", options=length_units)
    d_input = mo.ui.number(value = 2.625, label="Hole diameter: ")
    d_unit = mo.ui.dropdown(value="inch", options=length_units)
    d_pin_input = mo.ui.number(value = 2.5, label="Pin diameter: ")
    d_pin_unit = mo.ui.dropdown(value="inch", options=length_units)

    mo.vstack([mo.hstack([t_input, t_unit], justify="start"), 
               mo.hstack([w1_input, w1_unit], justify="start"),
               mo.hstack([w2_input, w2_unit], justify="start"),
               mo.hstack([h1_input, h1_unit], justify="start"),
               mo.hstack([h2_input, h2_unit], justify="start"),
               mo.hstack([d_input, d_unit], justify="start"),
               mo.hstack([d_pin_input, d_pin_unit], justify="start")], justify="center")
    return (
        d_input,
        d_pin_input,
        d_pin_unit,
        d_unit,
        h1_input,
        h1_unit,
        h2_input,
        h2_unit,
        t_input,
        t_unit,
        w1_input,
        w1_unit,
        w2_input,
        w2_unit,
    )


@app.cell(hide_code=True)
def _(
    d_input,
    d_pin_input,
    d_pin_unit,
    d_unit,
    h1_input,
    h1_unit,
    h2_input,
    h2_unit,
    t_input,
    t_unit,
    u,
    w1_input,
    w1_unit,
    w2_input,
    w2_unit,
):
    t = u.Quantity(t_input.value, t_unit.value)  # Thickness
    w1 = u.Quantity(w1_input.value, w1_unit.value)  # Width
    w2 = u.Quantity(w2_input.value, w2_unit.value)  # Width
    h1 = u.Quantity(h1_input.value, h1_unit.value)  # Height
    h2 = u.Quantity(h2_input.value, h2_unit.value)
    d = u.Quantity(d_input.value, d_unit.value)  # Hole Diameter
    d_pin = u.Quantity(d_pin_input.value, d_pin_unit.value)  # Pin Diameter
    return d, d_pin, h2, t, w1, w2


@app.cell
def _(mo):
    mo.md(r"""## Material Properties""")
    return


@app.cell(hide_code=True)
def _(mo):
    stress_units = ["ksi", "psi", "Pa", "MPa", "GPa"]
    Fu_input = mo.ui.number(value=58, label="Ultimate Tensile Strength Fu: ")
    Fu_unit = mo.ui.dropdown(value="ksi", options=stress_units)
    Fy_input = mo.ui.number(value=36, label="Yield Strength Fy: ")
    Fy_unit = mo.ui.dropdown(value="ksi", options=stress_units)

    mo.vstack([mo.hstack([Fu_input, Fu_unit], justify="start"),
               mo.hstack([Fy_input, Fy_unit], justify="start")])
    return Fu_input, Fu_unit, Fy_input, Fy_unit


@app.cell(hide_code=True)
def _(Fu_input, Fu_unit, Fy_input, Fy_unit, mo, u):
    # Material Properties - Assume A36 Steel
    Fu = u.Quantity(Fu_input.value, Fu_unit.value)
    Fy = u.Quantity(Fy_input.value, Fy_unit.value)
    Fa = min(Fu/5, Fy/3)
    mo.md(f"""
    Allowable Stress:

    Fa = {Fa:0.1f}
    """)
    return Fa, Fu, Fy


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Geometric Guidelines

    ### Rule 1
    """
    )
    return


@app.cell(hide_code=True)
def _(d, mo, os, w1, w2):
    _output = None
    a = min(w1, w2) - d/2
    if a >= d/2:
        _output = f'Lug satisfies Rule 1, a >= 1/2 * d'
    else:
        _output = f'Lug **DOES NOT** satisfy Rule 1, a < 1/2 * d.'
        if w1 <d:
            _output = _output + os.linesep*2 + f'Increase dimension w1 ({w1:0.3f}) to at least {d:0.3f}.'
        if w2 < d:
            _output = _output + os.linesep*2 + f'Increase dimension w2 ({w2:0.3f}) to at least {d:0.3f}.'
    mo.md(_output)
    return (a,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Rule 2""")
    return


@app.cell(hide_code=True)
def _(d, h2, mo, os):
    _output = None
    e = h2 - d/2
    if e >= 0.67 * d:
        _output = f'Lug satisfies Rule 2, e >= 0.67 * d.'
    else:
        _output = f'Lug **DOES NOT** satisfy Rule 2, e < 0.67 d.'
        _output = _output + os.linesep*2 + f'Increase dimension e to at least {0.67 * d:0.3f}.'
    mo.md(_output)
    return (e,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Evaluation based on Failure Modes

    AISC Code Checks per Section D.5.2
    """
    )
    return


@app.cell
def _(a, e, mo, os, t, u):
    _output = None
    _output = f'a = {a.to(u.inch):0.3f}'
    a_eff1 = 2 * t + 0.63 * u.inch
    a_eff2 = e / 1.33
    a_eff = min(a, a_eff1, a_eff2)
    _output = _output + os.linesep*2 + f'Evaluate based on a_eff = {a_eff.to(u.inch):0.3f}'
    mo.md(_output)
    return (a_eff,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Failure Mode 1

    Tension failure on both sides of the hole
    """
    )
    return


@app.cell
def _(Fa, Fu, Fy, WLL, a_eff, d, d_pin, mo, os, t, u):
    _output = None
    Pw1 = 2 * a_eff * t * Fa
    if d_pin / d >= 0.9:
        Cr = 1.0
    else:
        Cr = 1.0 - 0.275 * (1 - d_pin ** 2 / d ** 2) ** 0.5
    ae = min(a_eff, 4 * t, a_eff * 0.6 * Fu / Fy * (d / a_eff) ** 0.5)
    Pw11 = Cr * 2 * t * ae * Fa
    _output = f"""
    Maximum working load based on failure mode 1: {Pw1.to(u.lbf):0.0f}.

    Maximum working load BTH-1 alternative method: {Pw1.to(u.lbf):0.0f}.
    """
    if Pw1 >= WLL and Pw11 >= WLL:
        _output = _output + os.linesep*2 + '**OK!**'
    else:
        _output = _output + os.linesep*2 + '**NOT OK!**'
    mo.md(_output)    
    return (Cr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Failure Mode 2

    Bearing failure at the pin/lifting lug interface.
    """
    )
    return


@app.cell
def _(Fa, WLL, d_pin, mo, os, t, u):
    _output = None
    Pw2 = Fa * t * d_pin

    _output = f'Maximum working load based on failure mode 2: {Pw2.to(u.lbf):0.0f}.'
    if Pw2 >= WLL:
        _output = _output + os.linesep*2 + '**OK!**'
    else:
        _output = _output + os.linesep*2 + '**NOT OK!**'

    mo.md(_output)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Failure Mode 3
    Shear failure to edge of lug plate
    """
    )
    return


@app.cell
def _(Fa, WLL, d, d_pin, e, m, mo, os, t, u):
    _output = None
    Pw3 = 2 * Fa * e * t / 3**0.5

    # ASME BTH-1 alternative method
    phi = 55*u.degree * d_pin / d
    Av = 2 * (e + d_pin/2 * (1-m.cos(phi))) * t
    Pw31 = Av * Fa / 3**0.5

    _output = f"""
    Maximum working load based on failure mode 3: {Pw3.to(u.lbf):0.0f}.

    Maximum working BTH-1 alternative method: {Pw31.to(u.lbf):0.0f}.
    """

    if Pw3 >= WLL and Pw31 >= WLL:
        _output = _output + os.linesep*2 + '**OK!**'
    else:
        _output = _output + os.linesep*2 + '**NOT OK!**'

    mo.md(_output)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Failure Mode 4

    Single plane fracture failure
    """
    )
    return


@app.cell
def _(Cr, Fa, WLL, a_eff, d, e, mo, os, t, u):
    _output = None

    Pw4 = 1.67 * Fa * e ** 2 * t / d
    A_fracture = Cr * (1.13 * e + 0.92 * a_eff / (1 + a_eff / d)) * t
    Pw41 = A_fracture * Fa

    _output = f"""
    Maximum working load based on failure mode 4: {Pw4.to(u.lbf):0.0f}.

    Maximum working BTH-1 alternative method: {Pw41.to(u.lbf):0.0f}.
    """
    mo.md(f'')
    mo.md(f'')
    if Pw4 >= WLL and Pw41 >= WLL:
        _output = _output + os.linesep*2 + '**OK!**'
    else:
        _output = _output + os.linesep*2 + '**NOT OK!**'

    mo.md(_output)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Failure Mode 5

    Out-of-plane buckling failure of the lug
    """
    )
    return


@app.cell
def _(d, mo, os, t, u):
    _output = None
    if t > 0.5*u.inch:
        _output = f'Thickness is > 0.5 inch, **OK!**'
    else:
        _output = f'Increase thickness to 0.5 inch, **NOT OK!**'

    _output += os.linesep*2

    if t > 0.25 * d:
        _output += f'Thickness is > 0.25 * d, **OK!**'
    else:
        _output += f'Increase thickness to {0.25*d:0.3f}, **NOT OK!**'

    mo.md(_output)
    return


if __name__ == "__main__":
    app.run()
