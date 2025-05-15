// static/js/imageSelector.js

export function handleImageSelection(card, options = {}) {
    const src = card.querySelector('img').src;
    const title = card.dataset.title;
    const filename = card.dataset.filename;
    const id = card.dataset.id;
  
    if (options.imgElement) {
      options.imgElement.src = src;
      options.imgElement.classList.remove('d-none');
    }
  
    if (options.placeholderElement) {
      options.placeholderElement.classList.add('d-none');
    }

    if (options.placeholderIds) {
      for (let i = 0; i < options.placeholderIds.length; i++) {
        const el = document.getElementById(options.placeholderIds[i]);
        if (el) el.classList.add('d-none');
      }
    }
  
    if (options.labelElement) {
      options.labelElement.textContent = title;
    }
  
    if (options.inputElement && id) {
      options.inputElement.value = id;
    }
  
    if (options.resolutionElement && options.imgElement) {
      options.resolutionElement.innerHTML = options.imgElement.naturalWidth + 'x' + options.imgElement.naturalHeight + ' pixels';
    }
  
    if (options.fileTypeElement && filename) {
      options.fileTypeElement.innerHTML = filename.split('.').pop().toUpperCase();
    }
  
    if (options.iconElement && options.updateIcon) {
      options.iconElement.src = options.updateIcon;
    }
  
    if (typeof options.onImageSelected === 'function') {
      options.onImageSelected(src, title, filename);
    }
  }