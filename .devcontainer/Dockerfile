# FROM mambaorg/micromamba:latest
#
# COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/yy
#
# RUN micromamba install -y -n base -f /tmp/environment.yml && \
#     micromamba clean --all --yes

FROM mcr.microsoft.com/devcontainers/miniconda

COPY environment.yml /tmp/environment.yml

RUN /opt/conda/bin/conda env update -n base -f /tmp/environment.yml --solver=libmamba
