# Gunakan base image Alpine versi terbaru yang ringan dan resmi
FROM alpine:3.20

# Jangan gunakan root user secara langsung
ENV USERNAME=appuser
ENV HOME=/home/$USERNAME
ENV SHELL=/bin/bash

# Buat user dan group non-root, dan buat direktori kerja dengan permission terbatas
RUN apk add --no-cache bash \
    && addgroup -S $USERNAME \
    && adduser -S $USERNAME -G $USERNAME -h $HOME \
    && mkdir -p $HOME/app \
    && chown -R $USERNAME:$USERNAME $HOME \
    && chmod 700 $HOME

# Set working directory ke direktori home user non-root
WORKDIR $HOME/app

# Beralih ke user non-root
USER $USERNAME

# Set shell yang dipakai
SHELL ["/bin/bash", "-c"]

# Default command: jalankan bash interaktif
CMD ["bash"]

# Optional: healthcheck untuk memastikan container tetap hidup
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD pgrep bash || exit 1