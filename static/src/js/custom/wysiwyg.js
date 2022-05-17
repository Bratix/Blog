 
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

cash(".editor").each(function() {
    const el = this;
    let config = {
            toolbar: {
                items: [
                    'heading',
                    '|',
                    'bold',
                    'italic',
                    'link',
                    'bulletedList',
                    'numberedList',
                    '|',
                    'undo',
                    'redo',
                ]
            },
            table: {
                contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells']
            },
        };
  
    ClassicEditor.create(el, config).catch((error) => {
        console.error(error);
    });
});