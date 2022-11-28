import seaborn.objects as so
import palmerpenguins as pp

penguins = pp.load_penguins()

plot = (
    so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_g",
    )
    .add(so.Dot())
)
plot.show()
