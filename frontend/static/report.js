function downloadReport(filename="report", title="Field Service Report") {
    const doc = new jspdf.jsPDF('p', 'pt', 'a4');
    doc.autoTable({ html: '#reportTable', styles: {
        lineColor: [0, 0, 0],
        lineWidth: 1,
        }, theme: "grid",
        didDrawPage: function (data) {
            // Header
            doc.setFontSize(18);
            doc.text(title, data.settings.margin.left, 25);
          } })
    doc.save(`${filename}.pdf`)
}