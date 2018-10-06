class Price {}

enum Instrument {}

export class InstrumentsRepository {
    async prices(instrument: Instrument) {
        return fetch('');
    }
}
