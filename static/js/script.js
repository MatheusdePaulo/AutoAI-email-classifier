document.addEventListener('DOMContentLoaded', () => {
    // --- Seletores de Elementos ---
    const inputChoiceArea = document.getElementById('input-choice-area');
    const formInputArea = document.getElementById('form-input-area');
    const resultsArea = document.getElementById('results-area');

    const choiceTypeBtn = document.getElementById('choice-type');
    const choiceUploadBtn = document.getElementById('choice-upload');
    const backToChoiceBtn = document.getElementById('back-to-choice-button');

    const textareaWrapper = document.getElementById('textarea-wrapper');
    const uploadWrapper = document.getElementById('upload-wrapper');

    const emailForm = document.getElementById('emailForm');
    const emailContent = document.getElementById('emailContent');
    const emailFile = document.getElementById('emailFile');
    const fileNameSpan = document.getElementById('fileName');
    const processButton = document.getElementById('processButton');
    const loadingSpinner = document.querySelector('.is-loading-spinner');
    
    const categoryBox = document.getElementById('categoryBox');
    const resultCategory = document.getElementById('resultCategory');
    const categoryIcon = document.getElementById('categoryIcon');
    const responseBox = document.getElementById('responseBox');
    const resultResponse = document.getElementById('resultResponse');
    const copyResponseButton = document.getElementById('copyResponseButton');
    const copyResponseIcon = document.getElementById('copyResponseIcon'); // Novo seletor

    const debugInfo = document.getElementById('debugInfo');
    const toggleDebugButton = document.getElementById('toggleDebugButton');
    const rawClassificationOutput = document.getElementById('rawClassificationOutput');

    let currentInputMode = null;

    // --- Funções de Controle da UI ---
    
    function showFormFor(mode) {
        currentInputMode = mode;
        inputChoiceArea.style.display = 'none';
        formInputArea.style.display = 'block';

        if (mode === 'type') {
            textareaWrapper.style.display = 'block';
            uploadWrapper.style.display = 'none';
        } else if (mode === 'upload') {
            textareaWrapper.style.display = 'none';
            uploadWrapper.style.display = 'block';
        }
    }

    function showChoiceArea() {
        currentInputMode = null;
        inputChoiceArea.style.display = 'block';
        formInputArea.style.display = 'none';
        resultsArea.style.display = 'none';
        resetFormFields();
    }

    function resetFormFields() {
        emailContent.value = '';
        emailFile.value = '';
        fileNameSpan.textContent = 'Nenhum arquivo selecionado';
    }

    // --- Event Listeners ---

    choiceTypeBtn.addEventListener('click', () => showFormFor('type'));
    choiceUploadBtn.addEventListener('click', () => showFormFor('upload'));
    backToChoiceBtn.addEventListener('click', showChoiceArea);

    emailFile.addEventListener('change', function() {
        fileNameSpan.textContent = this.files.length > 0 ? this.files[0].name : 'Nenhum arquivo selecionado';
    });
    
    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // --- INÍCIO DA ANIMAÇÃO DE CARREGAMENTO ---
        resultsArea.style.display = 'block';
        resultCategory.textContent = 'Processando...';
        resultResponse.textContent = 'Gerando resposta...';
        
        // Aplica classes e ícones de loading
        [categoryBox, responseBox].forEach(box => {
            box.className = 'box result-box is-processing'; // Adiciona a classe da animação de pulsação
        });

        categoryIcon.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i>';
        copyResponseIcon.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i>'; // Troca o ícone de copiar por um spinner
        copyResponseButton.disabled = true;

        loadingSpinner.style.display = 'inline-block';
        processButton.disabled = true;
        backToChoiceBtn.disabled = true; // Desabilita o botão voltar durante o processamento

        let contentToSend;
        if (currentInputMode === 'type') {
            contentToSend = emailContent.value.trim();
        } else if (currentInputMode === 'upload' && emailFile.files.length > 0) {
            contentToSend = emailFile.files[0];
        }

        if (!contentToSend) {
            handleError(new Error('Nenhum conteúdo fornecido. Por favor, digite ou selecione um arquivo.'));
            return;
        }

        try {
            let emailText = '';
            if (typeof contentToSend === 'string') {
                emailText = contentToSend;
            } else {
                if (contentToSend.type !== 'text/plain') throw new Error('Formato de arquivo não suportado. Use .txt.');
                emailText = await contentToSend.text();
            }

            const response = await fetch('/classificar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email_content: emailText }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            updateUIWithResults(data);

        } catch (error) {
            handleError(error);
        }
    });
    
    function updateUIWithResults(data) {
        // --- FIM DA ANIMAÇÃO (SUCESSO) ---
        resultCategory.textContent = data.categoria;
        resultResponse.textContent = data.resposta_sugerida;
        rawClassificationOutput.textContent = JSON.stringify(data.raw_classification, null, 2);
        
        [categoryBox, responseBox].forEach(box => box.classList.remove('is-processing'));
        
        let statusClass = 'is-info', iconClass = 'fas fa-info-circle';
        if (data.categoria === 'Produtivo') {
            statusClass = 'is-success';
            iconClass = 'fas fa-check-circle';
        } else if (data.categoria === 'Não Classificado') {
            statusClass = 'is-warning';
            iconClass = 'fas fa-exclamation-triangle';
        }
        
        categoryBox.classList.add(statusClass);
        categoryIcon.innerHTML = `<i class="${iconClass}"></i>`;
        
        // Restaura ícone e botão de copiar
        copyResponseIcon.innerHTML = '<i class="fas fa-copy"></i>';
        copyResponseButton.disabled = false;
        loadingSpinner.style.display = 'none';
        processButton.disabled = false;
        backToChoiceBtn.disabled = false;
    }

    function handleError(error) {
        // --- FIM DA ANIMAÇÃO (ERRO) ---
        console.error('Erro:', error);
        resultCategory.textContent = 'Erro';
        resultResponse.textContent = error.message;
        
        [categoryBox, responseBox].forEach(box => {
            box.classList.remove('is-processing');
            box.classList.add('is-danger');
        });

        categoryIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
        
        // Restaura ícone e botão de copiar (mesmo em caso de erro)
        copyResponseIcon.innerHTML = '<i class="fas fa-copy"></i>';
        copyResponseButton.disabled = false;
        loadingSpinner.style.display = 'none';
        processButton.disabled = false;
        backToChoiceBtn.disabled = false;
    }

    copyResponseButton.addEventListener('click', async () => { 
        try {
            await navigator.clipboard.writeText(resultResponse.textContent);
            copyResponseButton.classList.add('is-success');
            setTimeout(() => copyResponseButton.classList.remove('is-success'), 1500);
        } catch (err) {
            console.error('Falha ao copiar texto: ', err);
        }
    });

    toggleDebugButton.addEventListener('click', () => {
        const isHidden = debugInfo.style.display === 'none';
        debugInfo.style.display = isHidden ? 'block' : 'none';
        toggleDebugButton.textContent = isHidden ? 'Esconder Debug' : 'Mostrar Debug';
    });
});