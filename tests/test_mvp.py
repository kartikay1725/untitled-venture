from app.services.mvp_generation import MVPGenerationService

def test_mvp_generation():
    class DummyIdea:
        description = "Test idea"
    blueprint = MVPGenerationService.generate(DummyIdea())
    assert blueprint.pdf_url.startswith("/")